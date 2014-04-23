
''' Logfile Meta worker '''
import hashlib
import datetime

class LogMetaData():
    ''' This worker computes a meta-data for log files. '''
    dependencies = ['sample', 'meta']

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']
        num_rows = raw_bytes.count('\n')
        head = raw_bytes[:100]
        tail = raw_bytes[-100:]
        output = {name:value for name,value in locals().iteritems()
                if name not in ['self', 'input_data','raw_bytes']}
        output.update(input_data['meta'])
        return output


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' log_meta.py: Unit test'''

    # Grab a sample
    sample = {'sample':{'raw_bytes':open('../../data/log/system.log', 'rb').read(), 'length':0,
              'filename': 'system.log', 'type_tag': 'pe', 'customer':'MegaCorp',
              'import_time':datetime.datetime.now()}}

    # Send it through meta
    import meta
    input_worker = meta.MetaData()
    _raw_output = input_worker.execute(sample)
    wrapped_output = {'meta':_raw_output}

    # Now join up the inputs
    wrapped_output.update(sample)

    worker = LogMetaData()

    import pprint
    pprint.pprint(worker.execute(wrapped_output))

if __name__ == "__main__":
    test()