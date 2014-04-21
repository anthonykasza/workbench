
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

    '''
    # Test out PEFile data
    file_list = [os.path.join('../data/pe/bad', child) for child in os.listdir('../data/pe/bad')]
    for filename in file_list:
        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'pe')
            results = c.work_request('view', md5)
            print 'Filename: %s results: %s' % (filename, results)
    '''

    # Test out zip data
    file_list = [os.path.join('../data/zip', child) for child in os.listdir('../data/zip')]
    for filename in file_list:
        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'zip')
            results = c.work_request('view', md5)
            print 'Filename: %s ' % (filename)
            pprint.pprint(results)

            # Or you could do this manually using leaf workers
            # The unzip worker gives you a list of md5s back
            # Run meta on all the unzipped files.
            results = c.work_request('unzip', md5)
            print '\n*** Filename: %s ***' % (filename)
            for child_md5 in results['unzip']['payload_md5s']:
                pprint.pprint(c.work_request('meta', child_md5))


def test():
    ''' simple_workbench_client test '''
    main()

if __name__ == '__main__':
    main()

