
''' Meta worker '''
import hashlib
import magic
import datetime

class MetaData():
    ''' This worker computes meta data for any file type. '''
    dependencies = ['sample']

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']
        md5 = hashlib.md5(raw_bytes).hexdigest()
        type_tag = input_data['sample']['type_tag']
        with magic.Magic() as m:
            file_type = m.id_buffer(raw_bytes[:1024])
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            mime_type = m.id_buffer(raw_bytes[:1024])
        with magic.Magic(flags=magic.MAGIC_MIME_ENCODING) as m:
            encoding = m.id_buffer(raw_bytes[:1024])
        file_size = len(raw_bytes)
        filename = input_data['sample']['filename']
        import_time = input_data['sample']['import_time']
        customer = input_data['sample']['customer']
        length = input_data['sample']['length']

        return {name:value for name,value in locals().iteritems()
                if name not in ['self', 'input_data','raw_bytes', 'm']}


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' meta.py: Unit test'''
    worker = MetaData()

    import pprint
    pprint.pprint(worker.execute({'sample':{'raw_bytes':open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(),
                    'length':0, 'filename': 'bad_033d91', 'type_tag': 'pe','customer':'MegaCorp',
                    'import_time':datetime.datetime.now()}}))

if __name__ == "__main__":
    test()