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
    parser.add_argument('-d', '--data-dir', type=str, default='../test_files/logs', help='Directory of files to import into the workbench server')
    parser.add_argument('-t', '--tag', type=str, default='log', help='Type_tag of the files being imported')
    args = parser.parse_args()

    # Connect to local workbench
    c = zerorpc.Client(heartbeat=None, timeout=300)
    c.connect("tcp://127.0.0.1:4242")
    
    # Grab all the filenames from the data directory
    data_dir = args.data_dir
    file_list = [os.path.join(data_dir, child) for child in os.listdir(data_dir)]

    # Upload the files into workbench
    for path in file_list:
        with open(path,'rb') as f:
            filename = os.path.basename(path)
            md5 = c.store_sample(filename, f.read(), args.tag)
            print 'Filename: %s uploaded... with type_tag: %s' % (filename, args.tag)

def test():
    ''' file_upload test '''
    main()

if __name__ == '__main__':
    main()

