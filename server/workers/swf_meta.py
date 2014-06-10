''' SWFMeta worker: This is a stub the real class (under the experimental 
                    directory has too many dependencies)
'''

class SWFMeta():
    ''' This worker computes a bunch of meta-data about a SWF file '''
    dependencies = ['sample', 'meta']

    def execute(self, input_data):

        # Get the raw_bytes
        raw_bytes = input_data['sample']['raw_bytes']

        # Add the meta data to the output
        output = input_data['meta']
        return output

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' swf_meta.py: Unit test'''
    
    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    md5 = c.store_sample('unknown.swf', open('../../data/swf/unknown.swf', 'rb').read(), 'pe')
    input_data = c.get_sample(md5)
    input_data.update(c.work_request('meta', md5))

    # Execute the worker
    worker = SWFMeta()
    output = worker.execute(input_data)
    print 'SWFMeta: '
    import pprint
    pprint.pprint(output)


if __name__ == "__main__":
    test()
