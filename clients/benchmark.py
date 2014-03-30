
import zerorpc
import os
import datetime

def main():

    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Benchmark test on PEFile test_files
    file_list = [os.path.join('../test_files/pe/bad', child) for child in os.listdir('../test_files/pe/bad')]
    file_list += [os.path.join('../test_files/pe/good', child) for child in os.listdir('../test_files/pe/good')]
    num_files = len(file_list)
    total_files = 0
    start = datetime.datetime.now()
    for i in xrange(10):
        for filename in file_list:
            with open(filename,'rb') as f:
                md5 = c.store_sample(filename, f.read(), 'pe')
                results = c.work_request('view', md5)
                print 'Filename: %s results: %s' % (filename, results)
        total_files += num_files
    end = datetime.datetime.now()
    delta = end - start
    print 'Files processed: %d  Time: %d seconds' % (total_files, delta.seconds)

def test():
    ''' benchmark test '''
    main()

if __name__ == '__main__':
    main()

