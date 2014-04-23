''' PcapMeta worker '''
import hashlib
import datetime
import struct

class PcapMeta():
    ''' This worker computes a bunch of meta-data about a pcap file '''
    dependencies = ['sample', 'meta']

    def execute(self, input_data):
        # Fixme: Put some PCAP specific Meta data here :)

        # Build up return data structure
        output = {name:value for name,value in locals().iteritems()
                if name not in ['self', 'input_data','raw_bytes']}
        output.update(input_data['meta'])
        return output

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pcap_meta.py: Unit test'''
    # Grab a sample
    sample = {'sample':{'raw_bytes':open('../../data/pcap/http.pcap', 'rb').read(), 'length':0,
              'filename': 'http.pcap', 'type_tag': 'pe', 'customer':'MegaCorp', 
              'import_time':datetime.datetime.now()}}

    # Send it through meta
    import meta
    input_worker = meta.MetaData()
    _raw_output = input_worker.execute(sample)
    wrapped_output = {'meta':_raw_output}

    # Now join up the inputs
    wrapped_output.update(sample)

    worker = PcapMeta()

    import pprint
    pprint.pprint(worker.execute(wrapped_output))


if __name__ == "__main__":
    test()
