
''' view_pcap_meta worker '''

def plugin_info():
    return {'name':'view_pcap_meta', 'class':'ViewPcap', 'dependencies': ['pcap_meta'],
            'description': 'This worker generates a pcap view for the sample. Output keys: [import_time, entropy, file_size, summary, sessions]'}

class ViewPcap():
    ''' ViewPcap: Generates a pcap view for the sample '''
    def execute(self, input_data):

        # Deprecation unless something more interesting happens with this class
        return input_data['pcap_meta']

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_pcap_meta.py: Unit test'''
    # This worker test requires a local server as it relies on the recursive dependencies
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    md5 = c.store_sample('http.pcap', open('../../data/pcap/http.pcap', 'rb').read(), 'pcap')
    output = c.work_request('view_pcap_meta', md5)
    print 'ViewPcap: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()