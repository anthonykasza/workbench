
''' view_meta worker '''

class ViewMetaData(object):
    ''' ViewMetaData: Generates a view for meta data on the sample '''
    dependencies = ['meta']

    def execute(self, input_data):

        # Deprecation unless something more interesting happens with this class
        return input_data['meta']

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_meta.py: Unit test'''
    # This worker test requires a local server as it relies on the recursive dependencies
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    md5 = c.store_sample('bad_067b39', open('../../data/pdf/bad/067b3929f096768e864f6a04f04d4e54', 'rb').read(), 'pdf')
    output = c.work_request('view_meta', md5)
    print 'ViewMetaData: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
