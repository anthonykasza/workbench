
''' Unzip worker '''
import StringIO
import zipfile
import zerorpc

def plugin_info():
    return {'name':'unzip', 'class':'Unzip', 'dependencies': ['sample'],
            'description': 'This worker unzips a zipped file. Output keys: [payload_md5s]'}

class Unzip():
    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']
        zipfile_output = zipfile.ZipFile(StringIO.StringIO(raw_bytes))
        payload_md5s = []
        for name in zipfile_output.namelist():
            payload_md5s.append(self.c.store_sample(name,zipfile_output.read(name), 'unknown'))
        return {'payload_md5s': payload_md5s}

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' unzip.py: Unit test'''
    worker = Unzip()
    output = worker.execute({'sample':{'raw_bytes':open('../../data/zip/bad.zip', 'rb').read()}})
    print 'Payloads extracted: %s ' % str(output['payload_md5s'])
    output = worker.execute({'sample':{'raw_bytes':open('../../data/zip/good.zip', 'rb').read()}})
    print 'Payloads extracted: %s ' % str(output['payload_md5s'])

if __name__ == "__main__":
    test()