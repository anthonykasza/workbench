
''' view_log_meta worker '''

class ViewLogMeta():
    ''' ViewLogMeta: Generates a view for meta data on the sample '''
    dependencies = ['log_meta']

    def execute(self, input_data):

        # Deprecation unless something more interesting happens with this class
        return input_data['log_meta']

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_log_meta.py: Unit test'''
    # This worker test requires a local server as it relies on the recursive dependencies
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    md5 = c.store_sample('system.log', open('../../data/log/system.log', 'rb').read(), 'log')
    output = c.work_request('view_log_meta', md5)
    print 'ViewLogMeta: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()