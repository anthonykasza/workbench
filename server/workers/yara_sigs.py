
''' Yara worker '''
import os, glob
import yara
import datetime

def plugin_info():
    return {'name':'yara_sigs', 'class':'YaraSigs', 'dependencies': ['sample'], 'description':'hi'}

class YaraSigs():
    ''' This worker check for matches against yara sigs. 
        Output keys: [matches:list of matches] '''

    def __init__(self):
        self.orig_dir = os.getcwd()
        self.rules = self.get_yara_rules()
        os.chdir(self.orig_dir)

    def get_yara_rules(self):

        # Try to find the yara rules directory relative to the worker
        if os.path.exists('yara/rules'):
            os.chdir('yara/rules')
        elif os.path.exists('workers/yara/rules'):
            os.chdir('workers/yara/rules')
        else:
            raise Exception('yara could not find yara rules directory under: %s' % os.getcwd())

        # Crawl all the .yar and .yara files in the directory and add them to the rules
        file_list = glob.glob('*.yar')
        file_list += glob.glob('*.yara')
        filepaths = {os.path.basename(sig_file):sig_file for sig_file in file_list}

        # Compile all the rules
        rules = yara.compile(filepaths=filepaths)
        return rules

    def mycallback(self, data):
	    print data
	    yara.CALLBACK_CONTINUE

    def execute(self, input_data):
        ''' yara worker execute method '''

        raw_bytes = input_data['sample']['raw_bytes']
        matches = self.rules.match_data(raw_bytes) #, callback=self.mycallback)
        return {'matches': matches}


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' yara.py: Unit test'''
    worker = YaraSigs()

    import pprint
    file_list = [os.path.join('../../test_files/pe/bad', child) for child in os.listdir('../../test_files/pe/bad')]
    for test_file in file_list:
	file_name = os.path.basename(test_file)
	print '\n%s' % file_name
	pprint.pprint(worker.execute({'sample':{'raw_bytes':open(test_file, 'rb').read(), 
	    'filename': file_name, 'type_tag': 'pe','import_time':datetime.datetime.now()}}))

if __name__ == "__main__":
    test()