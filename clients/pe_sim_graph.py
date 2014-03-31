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

def jaccard_sims(md5_list, feature_list):

    sim_info_list = []
    for index1, features1 in enumerate(feature_list):
        for index2, features2 in enumerate(feature_list):
            if index2 <= index1: continue
            sim = jaccard_sim(features1, features2)
            if sim > .5:
                sim_info_list.append({'source':md5_list[index1], 'target':md5_list[index2], 'sim':sim})

    return sim_info_list

def jaccard_sim(features1, features2):
    ''' Compute similarity between two sets using Jaccard similarity '''
    set1 = set(features1)
    set2 = set(features2)
    try:
        return len(set1.intersection(set2))/float(max(len(set1),len(set2)))
    except ZeroDivisionError:
        return 0
    #return len(set1.intersection(set2))/float(len(set1.union(set2)))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=4242, help='port used by workbench server')
    args = parser.parse_args()
    port = str(args.port)
    c = zerorpc.Client(timeout=300)
    c.connect('tcp://127.0.0.1:'+port)

    # Test out PEFile -> pe_deep_sim -> pe_jaccard_sim -> graph
    bad_files = [os.path.join('../test_files/pe/bad', child) for child in os.listdir('../test_files/pe/bad')]
    good_files = [os.path.join('../test_files/pe/good', child) for child in os.listdir('../test_files/pe/good')]
    
    # First throw them into workbench and add them as nodes into the graph
    bad_md5s = add_it(c, bad_files, ['pe','bad'])
    good_md5s = add_it(c, good_files, ['pe','good'])

    # Compute pe_deep_sim on all files of type pe
    results = c.batch_work_request('pe_deep_sim', {'type_tag': 'pe'})

    # Store the ssdeep sims as relationships
    for result in results:
        for sim_info in result['sim_list']:
            c.add_rel(result['md5'], sim_info['md5'], 'ssdeep')

    # Compute pe_features on all files of type pe, just pull back the sparse features
    results = c.batch_work_request('pe_features', {'type_tag': 'pe', 'subkeys':['md5','sparse_features.imported_symbols']})

    # Split out the md5 list and feature list
    md5_list = [r['md5'] for r in results]
    feature_list = [r['imported_symbols'] for r in results]

    # Compute the Jaccard Index between imported systems and store as relationships
    sims = jaccard_sims(md5_list, feature_list)
    for sim_info in sims:
        c.add_rel(sim_info['source'], sim_info['target'], 'imports')

    # Compute pe_features on all files of type pe, just pull back the sparse features
    results = c.batch_work_request('pe_features', {'type_tag': 'pe', 'subkeys':['md5','sparse_features.pe_warning_strings']})

    # Split out the md5 list and feature list
    md5_list = [r['md5'] for r in results]
    feature_list = [r['pe_warning_strings'] for r in results]

    # Compute the Jaccard Index between imported systems and store as relationships
    sims = jaccard_sims(md5_list, feature_list)
    for sim_info in sims:
        c.add_rel(sim_info['source'], sim_info['target'], 'warnings')

    # Compute pe_peid on all files of type pe, just pull back the match_list
    results = c.batch_work_request('pe_peid', {'type_tag': 'pe', 'subkeys':['md5','match_list']})

    # Split out the md5 list and feature list
    md5_list = [r['md5'] for r in results]
    feature_list = [r['match_list'] for r in results]

    # Compute the Jaccard Index between imported systems and store as relationships
    sims = jaccard_sims(md5_list, feature_list)
    for sim_info in sims:
        c.add_rel(sim_info['source'], sim_info['target'], 'peid')

    # Compute strings on all files of type pe, just pull back the string_list
    results = c.batch_work_request('strings', {'type_tag': 'pe', 'subkeys':['md5','string_list']})

    # Split out the md5 list and feature list
    md5_list = [r['md5'] for r in results]
    feature_list = [r['string_list'] for r in results]

    # Compute the Jaccard Index between imported systems and store as relationships
    sims = jaccard_sims(md5_list, feature_list)
    for sim_info in sims:
        c.add_rel(sim_info['source'], sim_info['target'], 'strings')

def test():
    ''' pe_peid test '''
    main()

if __name__ == '__main__':
    main()