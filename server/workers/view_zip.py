
''' view_zip worker '''
import zerorpc

class ViewZip(object):
    ''' ViewZip: Generates a view for Zip files '''
    dependencies = ['meta', 'unzip']

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):

        # Just a small check to make sure we haven't been called on the wrong file type
        if (input_data['meta']['mime_type'] != 'application/zip'):
            return {'error': self.__class__.__name__+': called on '+input_data['meta']['mime_type']}

        view = {}
        view['payload_md5s'] = input_data['unzip']['payload_md5s']
        view.update(input_data['meta'])

        # Okay this view is going to also give the meta data about the payloads
        view['payload_meta'] = [self.c.work_request('meta', md5) for md5 in input_data['unzip']['payload_md5s']]
        return view

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_zip.py: Unit test'''

    # This worker test requires a local server running
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    md5 = c.store_sample('bad.zip', open('../../data/zip/bad.zip', 'rb').read(), 'zip')

    input_data = c.work_request('meta', md5)
    input_data.update(c.work_request('unzip', md5))

    # Execute the worker
    worker = ViewZip()
    output = worker.execute(input_data)
    print 'ViewZip: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
