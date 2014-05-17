''' PcapSetBro worker '''
import os
import pcap_bro

class PcapSetBro(pcap_bro.PcapBro):
    ''' This worker runs Bro scripts on a set of pcap files '''
    dependencies = ['sample_sets']

    def pcap_inputs(self, input_data):
        
        # For PcapSetBro the input_data is expected to be set of md5s
        # Setup handles for the set of md5s.
        filenames = []
        for md5 in input_data['sample_sets']['md5_list']:
            sample = self.c.get_sample(md5)['sample']
            raw_bytes = sample['raw_bytes']
            filename = os.path.basename(sample['filename'])
            with open(filename,'wb') as pcap_file:
                pcap_file.write(raw_bytes)
                filenames.append(filename)
        return filenames


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pcap_set_bro.py: Unit test'''
    # This worker test requires a local server as it relies on the recursive dependencies
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Open a bunch of pcaps
    data_dir = '../../data/pcap'
    file_list = [os.path.join(data_dir, child) for child in os.listdir(data_dir)]
    pcap_md5s = []
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue        

        with open(filename,'rb') as f:
            pcap_md5s.append(c.store_sample(filename, f.read(), 'pcap'))

    # Now store the sample set
    set_md5 = c.store_sample_set(pcap_md5s)
    print set_md5

    # Execute the worker
    output = c.work_request('pcap_set_bro', set_md5)
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
