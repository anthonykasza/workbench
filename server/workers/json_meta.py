
''' JSON Meta worker '''
import json

class JSONMetaData(object):
    ''' This worker computes meta-data for json files. '''
    dependencies = ['sample', 'meta']

    def __init__(self):
        ''' Initialization '''
        self.meta = {}

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']

        # Take a peek at the JSON data
        data = json.loads(raw_bytes)
        self.meta['container'] = 'list' if isinstance(data, list) else 'dict'
        if self.meta['container'] == 'list':
            self.meta['list_length'] = len(data)
        else:
            self.meta['num_keys'] = len(data.keys())

        # Pull in meta data info as well
        self.meta.update(input_data['meta'])
        return self.meta


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' json_meta.py: Test '''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Store the sample
    md5 = c.store_sample('unknown.json', open('../../data/json/generated.json', 'rb').read(), 'json')

    # Execute the worker (server test)
    output = c.work_request('json_meta', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

    # Unit test stuff: Feel free to ignore
    input_data = c.get_sample(md5)
    input_data.update(c.work_request('meta', md5))

    # Execute the worker (unit test)
    worker = JSONMetaData()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
