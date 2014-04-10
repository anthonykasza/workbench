
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
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'pcap')
            results = c.work_request('pcap_bro', md5)

            # Results is just a dictionary of Bro log file names and their MD5s in workbench
            for log_name, md5 in results['pcap_bro'].iteritems():

                # Every workbench entry contains an md5 field (obviously not interested in that)
                if log_name == 'md5': continue

                bro_log = c.get_sample(md5)['sample']['raw_bytes']
                print '\n\n<<< Bro log: %s >>>\n %s' % (log_name, bro_log)
def test():
    ''' pcap_bro_raw test '''
    main()

if __name__ == '__main__':
    main()

