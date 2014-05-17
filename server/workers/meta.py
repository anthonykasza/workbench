
''' Meta worker '''
import hashlib
import magic
import datetime

class MetaData(object):
    ''' This worker computes meta data for any file type. '''
    dependencies = ['sample']

    def __init__(self):
        ''' Initialization '''
        self.meta = {}

    def execute(self, input_data):
        ''' This worker computes meta data for any file type. '''
        raw_bytes = input_data['sample']['raw_bytes']
        self.meta['md5'] = hashlib.md5(raw_bytes).hexdigest()
        self.meta['type_tag'] = input_data['sample']['type_tag']
        with magic.Magic() as mag:
            self.meta['file_type'] = mag.id_buffer(raw_bytes[:1024])
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as mag:
            self.meta['mime_type'] = mag.id_buffer(raw_bytes[:1024])
        with magic.Magic(flags=magic.MAGIC_MIME_ENCODING) as mag:
            self.meta['encoding'] = mag.id_buffer(raw_bytes[:1024])
        self.meta['file_size'] = len(raw_bytes)
        self.meta['filename'] = input_data['sample']['filename']
        self.meta['import_time'] = input_data['sample']['import_time']
        self.meta['customer'] = input_data['sample']['customer']
        self.meta['length'] = input_data['sample']['length']

        return self.meta


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' meta.py: Unit test'''
    worker = MetaData()

    import pprint
    pprint.pprint(worker.execute({'sample':{'raw_bytes':open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(),
                                            'length':0, 'filename': 'bad_033d91', 'type_tag': 'pe', 'customer':'MegaCorp',
                                            'import_time':datetime.datetime.now()}}))

if __name__ == "__main__":
    test()
