
''' view_pdffile worker '''

class ViewPDFFile():
    ''' ViewPDFFile: Generates a view for PDF files '''
    dependencies = ['meta', 'strings']

    def execute(self, input_data):

        # Just a small check to make sure we haven't been called on the wrong file type
        if (input_data['meta']['mime_type'] != 'application/pdf'):
            return {'error': self.__class__.__name__+': called on '+input_data['meta']['mime_type']}

        view = {}
        view['strings'] = input_data['strings']['string_list'][:5]
        view.update(input_data['meta'])
        return view

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    '''' view_pdf.py: Unit test'''
    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    md5 = c.store_sample('bad_067b392', open('../../data/pdf/bad/067b3929f096768e864f6a04f04d4e54', 'rb').read(), 'pdf')
    input_data = c.work_request('meta', md5)
    input_data.update(c.work_request('strings', md5))

    # Execute the worker (unit test)
    worker = ViewPDFFile()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)
    
    # Execute the worker (server test)
    output = c.work_request('view_pdf', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
