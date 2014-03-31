import zerorpc
import argparse
import os
import pprint


def add_it(c, file_list, labels):
    md5s = []
    for filename in file_list:
        if filename != '.DS_Store':
            with open(filename,'rb') as f:
                md5 = c.store_sample(filename,  f.read(), 'pe')
                c.add_node(md5, md5[:6], labels)
                md5s.append(md5)
    return md5s

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=4242, help='port used by workbench server')
    args = parser.parse_args()
    port = str(args.port)
    c = zerorpc.Client()
    c.connect('tcp://127.0.0.1:'+port)

    # Test out PEFile -> pe_deep_sim -> graph
    bad_files = [os.path.join('../test_files/pe/bad', child) for child in os.listdir('../test_files/pe/bad')]
    good_files = [os.path.join('../test_files/pe/good', child) for child in os.listdir('../test_files/pe/good')]
    
    # First throw them into workbench and add them as nodes into the graph
    bad_md5s = add_it(c, bad_files,['pe','bad'])
    good_md5s = add_it(c, good_files,['pe','good'])

    # Now store the graph of pe files as nodes and pe_deep_simimilarities as relationships
    results = c.batch_work_request('pe_deep_sim', {'type_tag': 'pe'})

    # Store the node and the ssdeep sims as relationships
    for result in results:
        for sim_info in result['sim_list']:
            c.add_rel(result['md5'], sim_info['md5'], 'ssdeep_sim')


def test():
    ''' pe_peid test '''
    main()

if __name__ == '__main__':
    main()