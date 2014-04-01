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
    parser.add_argument('-f', '--loadfile', type=str, default='../test_files/logs/system.log', help='File to import into the workbench server')
    args = parser.parse_args()

    # Connect to local workbench
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Upload the files into workbench
    my_file = args.loadfile
    with open(my_file,'rb') as f:

        # Check to see if workbench already has the file
        filename = os.path.basename(my_file)
        raw_bytes = f.read()
        md5 = c.store_sample(filename, raw_bytes, 'log')
        results = c.work_request('view', md5)
        print 'Filename: %s' % filename
        pprint.pprint(results)

def test():
    ''' file_upload test '''
    main()

if __name__ == '__main__':
    main()

