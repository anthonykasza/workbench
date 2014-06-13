
''' rekall_workbench: Helps with boilerplate to utilize the Rekall Memory Forensic Framework.
    See Google Github: https://github.com/google/rekall
    All credit for good stuff goes to them, all credit for bad stuff goes to us. :)
'''
import logging
from rekall import plugins
from rekall import session
from rekall.plugins.addrspaces import standard
from rekall.ui.renderer import BaseRenderer
import StringIO
import json
import datetime
import pprint

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
            s.GetParameter("profile")

        # Store session handle
        self.session = s

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
        ''' Just a stub method '''
        print 'Calling format on WorkbenchRenderer does nothing'

    def section(self, name=None, **kwargs):
        self.active_section = name
        self.output_data['sections'][self.active_section] = [] 

    def report_error(self, message):
        print 'Error Message: %s' % message

    def table_header(self, columns=None, **kwargs):
        self.active_headers = [col[0] for col in columns]

    def table_row(self, *args, **kwargs):
        self.output_data['sections'][self.active_section]. \
            append(self._cast_dict(dict(zip(self.active_headers, args))))

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

    def _cast_dict(self, data_dict):
        ''' Internal method that makes sure any dictionary elements
            are properly cast into the correct types, instead of
            just treating everything like a string from the csv file
        '''
        for key, value in data_dict.iteritems():
            data_dict[key] = self._cast_value(value)

        # Fixme: resp_body_data can be very large so removing it for now
        if 'resp_body_data' in data_dict:
            del data_dict['resp_body_data']

        return data_dict

    def _cast_value(self, value):
        ''' Internal method that makes sure any dictionary elements
            are properly cast into the correct types, instead of
            just treating everything like a string from the csv file
        '''
        # Try to convert to a datetime
        try:
            date_time = datetime.datetime.fromtimestamp(float(value))
            if date_time > datetime.datetime(2000, 1, 1) and \
               date_time < datetime.datetime(2020, 1, 1): # Fixme: Total Cheese Sauce
                raise ValueError
            else:
                return date_time

        # Next try a set of primitive types
        except (AttributeError, TypeError, ValueError):
            pass

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
