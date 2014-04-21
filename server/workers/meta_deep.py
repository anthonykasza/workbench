
''' MetaDeep worker '''
import hashlib
import ssdeep as ssd
import datetime

def plugin_info():
    return {'name':'meta_deep', 'class':'MetaDeepData', 'dependencies': ['sample', 'meta'],
            'description': 'This worker computes deeper meta-data. Output keys: [md5, sha1, sha256, ssdeep, entropy, file_type, mime_type, encoding, file_size, filename, import_time]'}

class MetaDeepData():

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']
        sha1 = hashlib.sha1(raw_bytes).hexdigest()
        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        ssdeep = ssd.hash(raw_bytes)
        entropy = self._entropy(raw_bytes)
        output = {name:value for name,value in locals().iteritems()
                if name not in ['self', 'input_data','raw_bytes']}
        output.update(input_data['meta'])
        return output

    def _entropy(self, s):
        # Grabbed this snippet from Rosetta Code (rosettacode.org)
        import math
        from collections import Counter
        p, lns = Counter(s), float(len(s))
        return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' meta_deep.py: Unit test'''

    # Grab a sample
    sample = {'sample':{'raw_bytes':open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(),
              'filename': 'bad_033d91', 'type_tag': 'pe','import_time':datetime.datetime.now()}}

    # Send it through meta
    import meta
    input_worker = meta.MetaData()
    _raw_output = input_worker.execute(sample)
    wrapped_output = {'meta':_raw_output}

    # Now join up the inputs
    wrapped_output.update(sample)

    worker = MetaDeepData()

    import pprint
    pprint.pprint(worker.execute(wrapped_output))

if __name__ == "__main__":
    test()