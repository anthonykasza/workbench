''' view_customer worker '''
import zerorpc

class ViewCustomer():
    ''' ViewCustomer: Generates a customer usage view. '''
    dependencies = ['meta']

    def execute(self, input_data):

        # View on all the meta data files in the sample
        fields = ['filename', 'md5', 'length', 'customer', 'import_time','type_tag']
        view = {key:input_data['meta'][key] for key in fields}
        return view

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_customer.py: Unit test'''
    # This worker test requires a local server as it relies on its dependencies
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    md5 = c.store_sample('bad_033d91', open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232','rb').read(), 'pe')
    output = c.work_request('view_customer', md5)
    print 'ViewCustomer: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
