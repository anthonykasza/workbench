''' SWFMeta worker: This code heavily utilizes https://github.com/timknip/pyswf, all credit for good
                    stuff goes to them, all credit for bad stuff goes to me. :)
'''
from swf.movie import SWF
import StringIO

def plugin_info():
    return {'name':'swf_meta', 'class':'SWFMeta', 'dependencies': ['sample', 'meta'],
            'description': 'This worker computes a bunch of meta-data about a pcap file. Output keys: [summary, sessions]'}

class SWFMeta():

    def execute(self, input_data):
        
        # Spin up SWF class
        swf = SWF()
        
        # Get the raw_bytes
        raw_bytes = input_data['sample']['raw_bytes']
        
        # Parse it
        swf.parse(StringIO.StringIO(raw_bytes))

        # Header info
        head = swf.header
        fields = ['version']
        output = {'version':head.version,'file_length':head.file_length,'frame_count':head.frame_count,
                  'frame_rate':head.frame_rate,'frame_size':head.frame_size.__str__(),'compressed':head.compressed}

        # Loop through all the tags
        output['tags'] = [tag.__str__() for tag in swf.tags]

        # Add the meta data to the output
        output.update(input_data['meta'])
        return output

        '''
        # Map all tag names to indexes
        tag_map = {tag.name:index for tag,index in enumerate(swf.tags)}

        # FileAttribute Info
        file_attr_tag = swf.tags[tag_map]
        
        '''
        '''

        # Build up return data structure
        output = {name:value for name,value in locals().iteritems()
                if name not in ['self', 'input_data','raw_bytes']}
        output.update(input_data['meta'])
        return output
        '''

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' swf_meta.py: Unit test'''
    
    # This worker test requires a local server as it relies heavily on the recursive dependencies
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    md5 = c.store_sample('unknown.swf', open('../../data/swf/unknown.swf', 'rb').read(), 'pe')
    output = c.work_request('swf_meta', md5)
    print 'SWFMeta: '
    import pprint
    pprint.pprint(output)


if __name__ == "__main__":
    test()
