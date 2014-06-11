
''' Benchmark that throws files at workbench with 4 subprocesses '''
import zerorpc
import os
import datetime
import multiprocessing

def main():
    ''' Benchmark that throws files at workbench with 4 subprocesses '''
    jobs = []
    args = ['../data/pe/bad', '../data/pe/good', '../data/pdf/bad', '../data/pdf/good']

    # These jobs are for stress testing
    for my_args in args:
        p = multiprocessing.Process(target=process_files, args=(my_args,))
        jobs.append(p)
        p.start()
    p.join()

    # This job is for test coverage
    process_files('../data/pe/bad')

def process_files(path):
    ''' Processes all the files within a directory '''

    # Cheesy, infer file_type based on path
    if 'pdf' in path:
        type_tag = 'pdf'
    else:
        type_tag = 'pe'

    # Open a connection to workbench
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Benchmark test on shoving data into workbench
    file_list = [os.path.join(path, child) for child in os.listdir(path)]
    num_files = len(file_list)
    total_files = 0
    start = datetime.datetime.now()
    for i in xrange(10):
        for filename in file_list:
            with open(filename, 'rb') as f:
                md5 = c.store_sample(filename, f.read(), type_tag)
                c.work_request('view', md5)
                print 'Filename: %s' % (filename)
        total_files += num_files
    end = datetime.datetime.now()
    delta = end - start
    print 'Files processed: %d  Time: %d seconds' % (total_files, delta.seconds)

    # Close the workbench connection
    c.close()

# Fixme: see https://github.com/SuperCowPowers/workbench/issues/40
def test():
    ''' stress_test test '''
    main()

if __name__ == '__main__':
    test()

