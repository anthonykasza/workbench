''' PE peid worker. Uses the peid_userdb.txt database of signatures.
'''
import sys
import peutils
import pefile
import pkg_resources

# Fixme: We want to load this once per module load
g_peid_sigs = pkg_resources.resource_string(__name__, 'peid_userdb.txt')

class PEIDWorker():
    ''' Create instance of PEIDWorker class. This class looks up signature for a PE file. '''
    dependencies = ['sample']

    def __init__(self):
        self.peid_sigs = g_peid_sigs

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']

        # Have the PE File module process the file
        try:
            pefile_handle = pefile.PE(data=raw_bytes,fast_load=False)
        except Exception, error:
            return {'error':  str(error), 'match_list': []}

        # Now get information from PEID module
        peid_match = self.peid_features(pefile_handle)
        return {'match_list': peid_match}

    def peid_features(self, pefile_handle):
        ''' Get features from PEid signature database'''
        signatures = peutils.SignatureDatabase(data = self.peid_sigs)
        peid_match = signatures.match(pefile_handle)
        return peid_match if peid_match else []

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pe_peid.py: Unit test'''
    worker = PEIDWorker()
    print worker.execute({'sample':{'raw_bytes':open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read()}})

if __name__ == "__main__":
    test()