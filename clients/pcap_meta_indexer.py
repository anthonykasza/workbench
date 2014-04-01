
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
    c = zerorpc.Client()
    c.connect(server+':'+port)

    # Test out PCAP test_files
    file_list = [os.path.join('../test_files/pcap', child) for child in os.listdir('../test_files/pcap')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'pcap')

            # Index the view_pcap_meta output (notice we can ask for any worker output)
            # Also (super important) it all happens on the server side.
            c.index_worker_output('view_pcap_meta', md5, 'view_pcap_meta')
            print '\n\n<<< PCAP Meta Data: %s Indexed>>>' % (filename)

def test():
    ''' pcap_meta_indexer test '''
    main()

if __name__ == '__main__':
    main()

