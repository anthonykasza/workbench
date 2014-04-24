''' view_pcap worker '''
import zerorpc
import itertools

class ViewPcap():
    ''' ViewPcap: Generates a view for a pcap sample (depends on Bro)'''
    dependencies = ['pcap_bro', 'pcap_meta']

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):

        # Loop around the output keys for pcap_meta and pcap_bro output
        view = {key: input_data['pcap_meta'][key] for key in input_data['pcap_meta'].keys()}

        # Grab logs from Bro
        view['bro_logs'] = {key: input_data['pcap_bro'][key] for key in input_data['pcap_bro'].keys() if '_log' in key}

        # Grab logs from Bro
        view['extracted_files'] = input_data['pcap_bro']['extracted_files']

        return view

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_pcap.py: Unit test'''
    # This worker test requires a local server as it relies on the recursive dependencies
    import zerorpc
    c = zerorpc.Client(timeout=300)
    c.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    md5 = c.store_sample('http.pcap', open('../../data/pcap/winmediaplayer.pcap', 'rb').read(), 'pcap')
    input_data = c.work_request('pcap_bro', md5)
    input_data.update(c.work_request('pcap_meta', md5))

    # Execute the worker
    worker = ViewPcap()
    output = worker.execute(input_data)
    print 'ViewPcap: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()