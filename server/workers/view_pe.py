
''' view_pe worker '''


class ViewPEFile(object):
    ''' Generates a high level summary view for PE files that incorporates a large set of workers '''
    dependencies = ['meta', 'strings', 'pe_peid', 'pe_indicators', 'pe_classifier', 'pe_disass']

    def execute(self, input_data):

        # Just a small check to make sure we haven't been called on the wrong file type
        if (input_data['meta']['mime_type'] != 'application/x-dosexec'):
            return {'error': self.__class__.__name__+': called on '+input_data['meta']['mime_type']}

        view = {}
        view['indicators']     = input_data['pe_indicators']['indicator_list']
        view['peid_Matches']   = input_data['pe_peid']['match_list']
        view['classification'] = input_data['pe_classifier']['classification']
        view['disass'] = self.safe_get(input_data, ['pe_disass', 'decode'])[:15]
        view.update(input_data['meta'])

        return view

    # Helper method
    @staticmethod
    def safe_get(data, key_list):
        ''' Safely access dictionary keys when plugin may have failed '''
        for key in key_list:
            data = data.get(key, {})
        return data if data else 'plugin_failed'

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_pe.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    md5 = c.store_sample('bad_033d91', open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(), 'pe')
    input_data = c.work_request('meta', md5)
    input_data.update(c.work_request('strings', md5))
    input_data.update(c.work_request('pe_peid', md5))
    input_data.update(c.work_request('pe_indicators', md5))
    input_data.update(c.work_request('pe_classifier', md5))
    # input_data.update(c.work_request('pe_disass', md5))

    # Execute the worker
    worker = ViewPEFile()
    output = worker.execute(input_data)
    print 'ViewPEFile: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
