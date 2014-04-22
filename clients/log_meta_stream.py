
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

    # Test out some log files
    file_list = [os.path.join('../data/log', child) for child in os.listdir('../data/log')]
    for filename in file_list:
        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'log')
            results = c.work_request('view_log_meta', md5)
            print 'Filename: %s\n' % (filename)
            pprint.pprint(results)
            stream_log = c.stream_sample(md5, 20)
            for row in stream_log:
                print row

def test():
    ''' log_meta_stream test '''
    main()

if __name__ == '__main__':
    main()

