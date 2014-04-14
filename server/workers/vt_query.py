
''' VTQuery worker '''
import zerorpc
import requests
import collections

def plugin_info():
    return {'name':'vt_query', 'class':'VTQuery', 'dependencies': ['meta'],
            'description': 'This worker query Virus Total, an apikey needs to be provided. Output keys: [positives, total, scan_date]'}

class VTQuery(object):
    
    def __init__(self):
        ''' VTQuery Init'''
        
        # Put your API Key here!
        self.apikey = None
        if not self.apikey:
            raise RuntimeError('VTQuery needs to be given an API key to work')
        
        # Change this if you want these fields
        self.exclude = ['scan_id', 'md5', 'sha1', 'sha256', 'resource', 'response_code', 'permalink',
                        'verbose_msg', 'scans']

    def execute(self, input_data):
        md5 = input_data['meta']['md5']
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', 
                                params={'apikey':self.apikey,'resource':md5, 'allinfo':1})
        vt_output = response.json()
        
        # Just pull some of the fields
        output = {field:vt_output[field] for field in vt_output.keys() if field not in self.exclude}
        
        # Check for not-found
        not_found = False if output else True        

        # Add in file_type
        output['file_type'] = input_data['meta']['file_type']
        
        # Toss back a not found
        if not_found:
            output['not_found'] = True
            return output

        # Organize the scans fields
        scan_results = collections.Counter()
        for scan in vt_output['scans'].values():
            if 'result' in scan:
                if scan['result']:
                    scan_results[scan['result']] += 1
        output['scan_results'] = scan_results.most_common(5)
        return output


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' vt_query.py: Unit test'''

    # This worker test requires a local server as it relies heavily on the recursive dependencies
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    md5 = c.store_sample('bad.zip', open('../../test_files/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(), 'pe')
    output = c.work_request('vt_query', md5)

    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()