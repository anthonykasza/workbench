
''' JSON Meta worker '''
import hashlib
import datetime
import json

def plugin_info():
    return {'name':'json_meta', 'class':'JSONMetaData', 'dependencies': ['sample', 'meta'],
            'description': 'This worker computes a meta-data for log files. Output keys: [md5, type_tag, file_type, mime_type, encoding, file_size, filename, import_time]'}

class JSONMetaData():

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

    # Grab a sample
    sample = {'sample':{'raw_bytes':open('../../data/json/generated.json', 'rb').read(),
              'filename': 'generated.json', 'type_tag': 'json','import_time':datetime.datetime.now()}}

    # Send it through meta
    import meta
    input_worker = meta.MetaData()
    _raw_output = input_worker.execute(sample)
    wrapped_output = {'meta':_raw_output}

    # Now join up the inputs
    wrapped_output.update(sample)

    worker = JSONMetaData()

    import pprint
    pprint.pprint(worker.execute(wrapped_output))

if __name__ == "__main__":
    test()