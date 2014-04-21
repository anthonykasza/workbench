
''' URLS worker: Tries to extract URL from strings output '''
import re

def plugin_info():
    return {'name':'urls', 'class':'URLS', 'dependencies': ['strings'],
            'description': 'This worker looks for url patterns in strings output. Output keys: [url_list]'}

class URLS():
    def __init__(self):
        self.url_match = re.compile(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', re.MULTILINE)

    def execute(self, input_data):
        string_output = input_data['strings']['string_list']
        flatten = ''.join(string_output)
        urls = self.url_match.findall(flatten)
        return {'url_list': urls}


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' url.py: Unit test'''
    import strings
    input_worker = strings.Strings()
    _raw_output = input_worker.execute({'sample':{'raw_bytes':open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', "rb").read()}})
    wrapped_output = {'strings':_raw_output}
    worker = URLS()
    print worker.execute(wrapped_output)

if __name__ == "__main__":
    test()