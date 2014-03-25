'''
This python class codifies a bunch of rules around suspicious static
features in a PE File. The rules don't indicate malicious behavior
they simply flag things that may be used by a malicious binary.
This class is currently a stub for future work... :)
'''

import re
import inspect
import pefile

def plugin_info():
    return {'name':'pe_indicators', 'class':'Indicators', 'dependencies': ['sample'],
            'description': 'This worker uses the static features from the pefile module to look for weird stuff.  Output keys: [indicator_list]'}

class Indicators():
    ''' Create instance of Indicators class. This class uses the
        static features from the pefile module to look for weird stuff.
        Note: All methods that start with 'check_' will be automatically
              included as part of the checks that happen when 'execute'
              is called.
    '''

    def __init__(self):
        ''' Init method of the Indicators class. '''
        self.pefile_handle = None

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']

        ''' Analyze the output of pefile for any anomalous conditions. '''
        # Have the PE File module process the file
        try:
            self.pefile_handle = pefile.PE(data=raw_bytes,fast_load=False)
        except Exception, error:
            return {'error': str(error), 'indicator_list': [{'Error': 'PE module failed!'}]}

        indicators = []
        indicators += [ {'description':warn,'severity':2, 'category':'PE_WARN'} for warn in self.pefile_handle.get_warnings()]

        # Automatically invoke any method of this class that starts with 'check_'
        check_methods = self._get_check_methods()
        for check_method in check_methods:
            hit_data = check_method()
            if (hit_data):
                indicators.append(hit_data)

        return {'indicator_list':indicators}

    #
    # Check methods
    #
    def check_checksum_is_zero(self):
        ''' Checking for a checksum of zero '''
        if (self.pefile_handle.OPTIONAL_HEADER):
            if (not self.pefile_handle.OPTIONAL_HEADER.CheckSum):
                return {'description':'Checksum of Zero','severity':1, 'category':'MALFORMED'}
        return None

    def check_checksum_mismatch(self):
        ''' Checking for a checksum that doesn't match the generated checksum '''
        if (self.pefile_handle.OPTIONAL_HEADER):
            if (self.pefile_handle.OPTIONAL_HEADER.CheckSum != self.pefile_handle.generate_checksum()):
                return {'description':'Reported Checksum does not match actual checksum','severity':2, 'category':'MALFORMED'}
        return None

    def _get_check_methods(self):
        results = []
        for key in dir(self):
            try:
                value = getattr(self, key)
            except AttributeError:
                continue
            if (inspect.ismethod(value) and key.startswith('check_')):
                results.append(value)
        return results

# Helper functions
def convertToUTF8(s):
    if (isinstance(s, unicode)):
        return s.encode( "utf-8" )
    try:
        u = unicode( s, "utf-8" )
    except:
        return str(s)
    utf8 = u.encode( "utf-8" )
    return utf8

def convertToAsciiNullTerm(s):
    s = s.split('\x00', 1)[0]
    return s.decode('ascii', 'ignore')

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pe_indicators.py: Unit test'''
    worker = Indicators()
    print worker.execute({'sample':{'raw_bytes':open('../../test_files/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read()}})

if __name__ == "__main__":
    test()