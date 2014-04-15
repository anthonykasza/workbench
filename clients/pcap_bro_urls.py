
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

    # Loop through all the pcaps and collect a set of urls(hosts) from the http_log files
    urls = set()
    file_list = [os.path.join('../test_files/pcap', child) for child in os.listdir('../test_files/pcap')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as file:
            pcap_md5 = c.store_sample(filename, file.read(), 'pcap')
            results = c.work_request('pcap_bro', pcap_md5)

            # Just grab the http log
            if 'http_log' in results['pcap_bro']:
                log_md5 = results['pcap_bro']['http_log']
                http_data = c.stream_sample(log_md5, None)  # None Means all data
                urls = set( row['host'] for row in http_data)
                print '<<< %s >>>' % filename
                pprint.pprint(list(urls))
                print


def test():
    ''' pcap_bro_urls test '''
    main()

if __name__ == '__main__':
    main()

