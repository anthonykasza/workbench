
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

    # Loop through all the pcaps and collect a set of urls(hosts) from the bro_log_http files
    urls = set()
    file_list = [os.path.join('../test_files/pcap', child) for child in os.listdir('../test_files/pcap')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'pcap')
            results = c.work_request('pcap_bro', md5)

            # Results is just a dictionary of Bro log file names and their MD5s in workbench
            for log_name, md5 in results['pcap_bro'].iteritems():

                # Just grab the http log
                if log_name == 'bro_log_http':
                    bro_log_data = c.stream_sample(md5, None)  # None Means all data
                    for row in bro_log_data:
                        urls.add(row['host'])

    print '<<< Unique URLs(Hosts) seen in PCAPS'
    print urls

def test():
    ''' pcap_urls test '''
    main()

if __name__ == '__main__':
    main()

