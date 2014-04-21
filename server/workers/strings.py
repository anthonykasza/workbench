
''' Strings worker '''
import re

def plugin_info():
    return {'name':'strings', 'class':'Strings', 'dependencies': ['sample'],
            'description': 'This worker extracts all the strings from any type of file. Output keys: [string_list]'}

class Strings():
    def __init__(self):
        self.find_strings = re.compile(r'[^\x00-\x1F\x7F-\xFF]{4,}', re.MULTILINE)

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']
        strings = self.find_strings.findall(raw_bytes)
        return {'string_list': strings}

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' strings.py: Unit test'''
    worker = Strings()
    print worker.execute({'sample':{'raw_bytes':open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', "rb").read()}})

if __name__ == "__main__":
    test()