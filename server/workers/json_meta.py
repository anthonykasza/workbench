
''' JSON Meta worker '''
import hashlib
import datetime
import json

class JSONMetaData():
    ''' This worker computes a meta-data for json files. '''
    dependencies = ['sample', 'meta']

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']

        # Take a peek at the JSON data
        data = json.loads(raw_bytes)
        json_container = 'list' if isinstance(data, list) else 'dict'
        if json_container == 'list':
            json_list_length = len(data)
        else:
            json_num_keys = len(data.keys())

        output = {name:value for name,value in locals().iteritems()
                if name not in ['self', 'input_data','raw_bytes', 'data']}
        output.update(input_data['meta'])
        return output


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' json_meta.py: Unit test'''

    # This worker test requires a local server as it relies heavily on the recursive dependencies
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    md5 = c.store_sample('unknown.swf', open('../../data/json/generated.json', 'rb').read(), 'json')
    input_data = c.get_sample(md5)
    input_data.update(c.work_request('meta', md5))

    # Execute the worker
    worker = JSONMetaData()
    output = worker.execute(input_data)
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()