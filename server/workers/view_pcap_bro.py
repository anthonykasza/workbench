''' view_pcap_bro worker '''
import zerorpc
import itertools


def plugin_info():
    return {'name':'view_pcap_bro', 'class':'ViewPcapBro', 'dependencies': ['pcap_bro', 'pcap_meta'],
            'description': 'This worker generates a pcap view for the sample. Output keys: [bro_output_log_names...]'}

class ViewPcapBro():
    ''' ViewPcapBro: Generates a view for bro output on a pcap sample '''
    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):

        # Loop around the output keys for pcap_meta and pcap_bro output
        view = {key: input_data['pcap_bro'][key] for key in input_data['pcap_bro'].keys()}
        view.update({key: input_data['pcap_meta'][key] for key in input_data['pcap_meta'].keys()})

        # Okay this view is going to also take a peek at the bro output logs
        for name, md5 in input_data['pcap_bro'].iteritems():
            if '_log' in name:
                view[name] = []
                stream = self.c.stream_sample(md5, 20)
                for row in itertools.islice(stream, 0, 1):
                    view[name].append(row)
        return view

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_pcap_bro.py: Unit test'''
    # This worker test requires a local server as it relies on the recursive dependencies
    import zerorpc
    c = zerorpc.Client(timeout=300)
    c.connect("tcp://127.0.0.1:4242")

    md5 = c.store_sample('http.pcap', open('../../test_files/pcap/http.pcap', 'rb').read(), 'pcap')
    output = c.work_request('view_pcap_bro', md5)
    print 'ViewPcapBro: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()