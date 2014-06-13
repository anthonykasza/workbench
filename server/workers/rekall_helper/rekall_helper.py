
''' rekall_workbench: Helps with boilerplate to utilize the Rekall Memory Forensic Framework.
    See Google Github: https://github.com/google/rekall
    All credit for good stuff goes to them, all credit for bad stuff goes to us. :)
'''
import logging
from rekall import plugins
from rekall import session
from rekall.plugins.addrspaces import standard
from rekall.ui.renderer import BaseRenderer
from rekall.ui.renderer import Formatter
import StringIO
import json
import datetime
import pprint
import msgpack
import pytz
import collections

class MemSession(object):
    ''' MemSession: Helps utilize the Rekall Memory Forensic Framework. '''

    def __init__(self, raw_bytes):
        ''' Create a Rekall session from raw_bytes '''

        # Spin up the logging
        logging.getLogger().setLevel(logging.ERROR)

        # Open up a rekall session
        s = session.Session(profile_path=["http://profiles.rekall-forensic.com"])

        # Set up a memory space for our raw memory image
        with s:
            mem_file = StringIO.StringIO(raw_bytes)
            s.physical_address_space = standard.FDAddressSpace(fhandle=mem_file, session=s)
            profile = s.GetParameter("profile")

        # Store session handle
        self.session = s

        # Pack the session (testing for now)
        #packed = msgpack.packb(self.session, use_bin_type=True)
        #print 'Size of packed session %d' % packed.sized
        #self.session = msgpack.unpackb(packed, encoding='utf-8')
        

    def get_session(self):
        ''' Get the current session handle '''
        return self.session


class WorkbenchRenderer(BaseRenderer):
    ''' Workbench Renderer: Extends BaseRenderer and simply populates local python
        data structures, not meant to be serialized or sent over the network. '''

    def __init__(self):
        self.output_data = None
        self.active_section = None
        self.active_headers = None
        self.header_types = None
        self.incoming_section = False
        self.formatter = Formatter()

    def start(self, plugin_name=None, kwargs=None):
        ''' Start method: initial data structures and store some meta data '''
        self.output_data = {'sections':{}}
        self.section('Info')        
        self.output_data['plugin_name'] = plugin_name
        return self

    def end(self):
        ''' Just a stub method '''
        print 'Calling end on WorkbenchRenderer does nothing'

    def format(self, formatstring, *args):

        # Make a new section
        if self.incoming_section:
            section_name = self.formatter.format(formatstring, *args).strip()
            self.section(section_name)
            self.incoming_section = False
        else:
            print 'Format called with %s' % self.formatter.format(formatstring, *args)

    def section(self, name=None, **kwargs):

        # Check for weird case where an section call is made wit
        # no name and then a format call is made
        if not name:
            self.incoming_section = True
            return

        # Create a new section and make it the active one
        self.active_section = name
        self.output_data['sections'][self.active_section] = [] 

    def report_error(self, message):
        print 'Error Message: %s' % message

    def table_header(self, columns=None, **kwargs):
        self.active_headers = [col[0] for col in columns]
        self.header_types = [col[1] for col in columns]

    def table_row(self, *args, **kwargs):
        self.output_data['sections'][self.active_section]. \
            append(self._cast_row(self.active_headers, args, self.header_types))

    def write_data_stream(self):
        ''' Just a stub method '''
        print 'Calling write_data_stream on WorkbenchRenderer does nothing'

    def flush(self):
        ''' Just a stub method '''
        print 'Calling flush on WorkbenchRenderer does nothing'

    def render(self, plugin):
        self.start(plugin_name=plugin.name)
        plugin.render(self)
        return self.output_data

    def _cast_row(self, keys, values, data_types):
        ''' Internal method that makes sure that the row elements
            are properly cast into the correct types, instead of
            just treating everything like a string from the csv file
        '''
        output_dict = collections.OrderedDict()
        for key, value, dtype in zip(keys, values, data_types):
            output_dict[key] = self._cast_value(value, dtype)

        return output_dict

    def _cast_value(self, value, dtype):
        ''' Internal method that makes sure any dictionary elements
            are properly cast into the correct types, instead of
            just treating everything like a string from the csv file
        '''

        # Try to convert to a datetime
        if 'time' in dtype:
            date_time = value.as_datetime()
            if date_time == datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.utc): # Special case
                return '-'
            return date_time

        # Rekall puts a bunch of data_modeling semantics that we're just ignoring for now :(
        value = str(value)

        # Try conversion to basic types
        tests = (int, float, str)
        for test in tests:
            try:
                return test(value)
            except (AttributeError, ValueError):
                continue
        return value


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' rekall_helper.py: Test '''

    # Grab the sample bytes
    with open('/Users/briford/volatility/mem_images/exemplar4.vmem', 'rb') as mem_file:
        raw_bytes = mem_file.read()

        MemS = MemSession(raw_bytes)
        renderer = WorkbenchRenderer()

        s = MemS.get_session()
        plugin = s.plugins.imageinfo()
        output = renderer.render(s.plugins.imageinfo())
        pprint.pprint(output)

        output = renderer.render(s.plugins.pslist())
        pprint.pprint(output)

if __name__ == "__main__":
    test()
