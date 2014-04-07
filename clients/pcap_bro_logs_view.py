
import zerorpc
import os
import pprint
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=4242, help='port used by workbench server')
    parser.add_argument('-s', '--server', type=str, default='tcp://127.0.0.1', help='location of workbench server')
    args = parser.parse_args()
    port = str(args.port)
    server = str(args.server)
    c = zerorpc.Client(timeout=300)
    c.connect(server+':'+port)

    # Test out getting the raw Bro logs from a PCAP file
    # Note: you can get a super nice 'generator' python list of dict by using
    #       'stream_sample' instead of 'get_sample'.
    file_list = [os.path.join('../test_files/pcap', child) for child in os.listdir('../test_files/pcap')]
    #data_dir = '/Users/briford/data/pcaps/threatglass'
    #file_list = [os.path.join(data_dir, child) for child in os.listdir(data_dir)]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        # Process the pcap file
        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'pcap')
            results = c.work_request('view_pcap_bro', md5)
            print '\n<<< %s >>>' % filename
            pprint.pprint(results)

def test():
    ''' pcap_bro_logs_view test '''
    main()

if __name__ == '__main__':
    main()

