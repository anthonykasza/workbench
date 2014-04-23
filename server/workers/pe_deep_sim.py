
''' PE SSDeep Similarity worker '''
import ssdeep as ssd
import zerorpc
from operator import itemgetter

class PEDeepSim():
    ''' This worker computes fuzzy matches between samples with ssdeep '''
    dependencies = ['meta_deep']

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):
        ''' Execute method '''
        my_ssdeep = input_data['meta_deep']['ssdeep']
        my_md5 = input_data['meta_deep']['md5']

        # For every PE sample in the database compute my ssdeep fuzzy match
        results = self.c.batch_work_request('meta_deep', {'type_tag':'pe','subkeys':['md5','ssdeep']})
        sim_list = []
        for result in results:
            if result['md5'] != my_md5:
                sim_list.append({'md5':result['md5'], 'sim':ssd.compare(my_ssdeep, result['ssdeep'])})

        # Sort and return the sim_list (with some logic for threshold)
        sim_list.sort(key=itemgetter('sim'), reverse=True)
        output_list = [sim for sim in sim_list if sim['sim'] > 0]
        return {'md5': my_md5, 'sim_list':output_list}

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pe_deep_sim.py: Unit test '''
    # This worker test requires a local server as it relies heavily on the recursive dependencies
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    md5 = c.store_sample('bad_067b392', open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(), 'pe')
    output = c.work_request('pe_deep_sim', md5)
    print 'SSDeep Similarities: '
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()