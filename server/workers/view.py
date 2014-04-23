
''' view worker '''
import zerorpc

class View():
    ''' View: Generates a view for any file type '''
    dependencies = ['meta']

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):

        # Grab the mime_type from the input and switch view types
        md5 = input_data['meta']['md5']
        mime_type = input_data['meta']['mime_type']
        if mime_type == 'application/x-dosexec':
            result = self.c.work_request('view_pe', md5)
        elif mime_type == 'application/pdf':
            result = self.c.work_request('view_pdf', md5)
        elif mime_type == 'application/zip':
            result = self.c.work_request('view_zip', md5)
        elif mime_type == 'application/vnd.tcpdump.pcap':
            result = self.c.work_request('view_pcap_meta', md5)
        elif mime_type == 'application/x-shockwave-flash':
            result = self.c.work_request('swf_meta', md5)
        else:
            # In the case of an unsupported MIME type just return the meta data
            result = input_data

        return result

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view.py: Unit test'''
    import pprint

    # This worker test requires a local server as it relies heavily on the recursive dependencies
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    md5 = c.store_sample('bad_067b39', open('../../data/pdf/bad/067b3929f096768e864f6a04f04d4e54', 'rb').read(), 'pdf')
    output = c.work_request('view', md5)
    print '\nView: '
    pprint.pprint(output)
    md5 = c.store_sample('bad_033d91', open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(), 'pe')
    output = c.work_request('view', md5)
    print '\nView: '
    pprint.pprint(output)
    md5 = c.store_sample('good.zip', open('../../data/zip/good.zip', 'rb').read(), 'zip')
    output = c.work_request('view', md5)
    print '\nView: '
    pprint.pprint(output)
    md5 = c.store_sample('workbench.py', open('../../server/workbench.py', 'rb').read(), 'python')
    output = c.work_request('view', md5)
    print '\nView: '
    pprint.pprint(output)

if __name__ == "__main__":
    test()