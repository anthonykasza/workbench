
''' Logfile Meta worker '''
import hashlib
import datetime

class LogMetaData():
    ''' This worker computes a meta-data for log files. '''
    dependencies = ['sample', 'meta']

    def __init__(self):
        ''' Initialization '''
        self.meta = {}

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']
        self.meta['num_rows'] = raw_bytes.count('\n')
        self.meta['head'] = raw_bytes[:100]
        self.meta['tail'] = raw_bytes[-100:]
        self.meta.update(input_data['meta'])
        return self.meta


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' log_meta.py: Unit test'''
    # This worker test requires a local server as it relies heavily on the recursive dependencies
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    md5 = c.store_sample('bad_067b392', open('../../data/log/system.log', 'rb').read(), 'log')
    input_data = c.get_sample(md5)
    input_data.update(c.work_request('meta', md5))

    # Execute the worker (unit test)
    worker = LogMetaData()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # Execute the worker (server test)
    output = c.work_request('log_meta', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()