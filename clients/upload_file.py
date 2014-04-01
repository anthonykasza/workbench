import zerorpc
import os
import pprint
import hashlib
import argparse


'''
def md5_for_file(path, block_size=256*128):
    md5 = hashlib.md5()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()
'''

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, default='../test_files/logs/system.log', help='File to inport into the workbench server')
    args = parser.parse_args()

    c = zerorpc.Client(heartbeat=None, timeout=300)
    c.connect("tcp://127.0.0.1:4242")

    # Upload the file into workbench
    with open(args.file,'rb') as file:

        # Check to see if workbench already has the file
        filename = os.path.basename(args.file)
        raw_bytes =  file.read()
        md5 = c.store_sample(filename, raw_bytes, 'log')
        results = c.work_request('view', md5)
        print 'Filename: %s' % filename
        pprint.pprint(results)

def test():
    ''' file_upload test '''
    main()

if __name__ == '__main__':
    main()

