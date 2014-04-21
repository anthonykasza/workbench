import zerorpc
import argparse
import os
import pprint

def main():


    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=4242, help='port used by workbench server')
    args = parser.parse_args()
    port = str(args.port)
    c = zerorpc.Client()
    c.connect('tcp://127.0.0.1:'+port)

    # Test out PEFile -> peid
    file_list = [os.path.join('../data/pe/bad', child) for child in os.listdir('../data/pe/bad')]
    file_list += [os.path.join('../data/pe/good', child) for child in os.listdir('../data/pe/good')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'pe')
            results = c.work_request('pe_peid', md5)
            pprint.pprint(results)


def test():
    ''' pe_peid test '''
    main()

if __name__ == '__main__':
    main()