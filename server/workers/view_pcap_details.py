''' view_pcap_details worker '''
import zerorpc
import itertools
import view_pcap

class ViewPcapDetails():
    ''' ViewPcapDetails: Generates a view for a pcap sample (depends on Bro)'''
    dependencies = ['view_pcap']

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):
        
        # Copy info from input
        view = input_data['view_pcap']
        
        # Grab a couple of handles
        extracted_files = input_data['view_pcap']['extracted_files']
        bro_logs = input_data['view_pcap']['bro_logs']
        
        # Dump a couple of fields
        del view['extracted_files']        

        # Gather additional info from the Bro logs
        '''
        view['bro_log_meta'] = [self.c.work_request('meta', md5) for md5 in bro_logs]
        '''

        # Grab additional info about the extracted files
        view['extracted_files'] = [self.c.work_request('meta_deep', md5, 
            ['md5','sha256','entropy','ssdeep','file_size','file_type']) for md5 in extracted_files]


        '''
        # Okay this view is going to also take a peek at the bro output logs
        for name, md5 in input_data['pcap_bro'].iteritems():
            if '_log' in name:
                view[name] = []
                stream = self.c.stream_sample(md5, 20)
                for row in itertools.islice(stream, 0, 1):
                    view[name].append(row)
        '''
        return view

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_pcap_details.py: Unit test'''
    # This worker test requires a local server as it relies on the recursive dependencies
    import zerorpc
    c = zerorpc.Client(timeout=300)
    c.connect("tcp://127.0.0.1:4242")

    md5 = c.store_sample('http.pcap', open('../../data/pcap/winmediaplayer.pcap', 'rb').read(), 'pcap')
    output = c.work_request('view_pcap_details', md5)
    print 'ViewPcapDetails: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()