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

def jaccard_sims(feature_list):

    sim_info_list = []
    for feature_info in feature_list:
        md5_source = feature_info['md5']
        features_source = feature_info['features']
        for feature_info in feature_list:
            md5_target = feature_info['md5']
            features_target = feature_info['features']
            if md5_source == md5_target: continue
            sim = jaccard_sim(features_source, features_target)
            if sim > .5:
                sim_info_list.append({'source':md5_source, 'target':md5_target, 'sim':sim})

    return sim_info_list

def jaccard_sim(features1, features2):
    ''' Compute similarity between two sets using Jaccard similarity '''
    set1 = set(features1)
    set2 = set(features2)
    try:
        return len(set1.intersection(set2))/float(max(len(set1),len(set2)))
    except ZeroDivisionError:
        return 0

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=4242, help='port used by workbench server')
    args = parser.parse_args()
    port = str(args.port)
    c = zerorpc.Client()
    c.connect('tcp://127.0.0.1:'+port)


    # Test out PEFile -> pe_deep_sim -> pe_jaccard_sim -> graph
    bad_files = [os.path.join('../data/pe/bad', child) for child in os.listdir('../data/pe/bad')]
    good_files = [os.path.join('../data/pe/good', child) for child in os.listdir('../data/pe/good')]
    
    # First throw them into workbench and add them as nodes into the graph
    bad_md5s = add_it(c, bad_files, ['pe','bad'])
    good_md5s = add_it(c, good_files, ['pe','good'])


    # Compute pe_features on all files of type pe, just pull back the sparse features
    imports = c.batch_work_request('pe_features', {'type_tag': 'pe', 'subkeys':['md5','sparse_features.imported_symbols']})

    # Compute pe_features on all files of type pe, just pull back the sparse features
    warnings = c.batch_work_request('pe_features', {'type_tag': 'pe', 'subkeys':['md5','sparse_features.pe_warning_strings']})
    
    # Compute strings on all files of type pe, just pull back the string_list
    strings = c.batch_work_request('strings', {'type_tag': 'pe', 'subkeys':['md5','string_list']})
    
    # Compute pe_peid on all files of type pe, just pull back the match_list
    peids = c.batch_work_request('pe_peid', {'type_tag': 'pe', 'subkeys':['md5','match_list']})    

    # Organize the data a bit
    imports = [{'md5':r['md5'],'features':r['imported_symbols']} for r in imports]
    warnings = [{'md5':r['md5'],'features':r['pe_warning_strings']} for r in warnings]
    strings = [{'md5':r['md5'],'features':r['string_list']} for r in strings]
    peids = [{'md5':r['md5'],'features':r['match_list']} for r in peids]
    

    # Compute the Jaccard Index between imported systems and store as relationships
    sims = jaccard_sims(imports)
    for sim_info in sims:
        c.add_rel(sim_info['source'], sim_info['target'], 'imports')

    # Compute the Jaccard Index between warnings and store as relationships
    sims = jaccard_sims(warnings)
    for sim_info in sims:
        c.add_rel(sim_info['source'], sim_info['target'], 'warnings')

    # Compute the Jaccard Index between strings and store as relationships
    sims = jaccard_sims(strings)
    for sim_info in sims:
        c.add_rel(sim_info['source'], sim_info['target'], 'strings')

    # Compute the Jaccard Index between peids and store as relationships
    sims = jaccard_sims(peids)
    for sim_info in sims:
        c.add_rel(sim_info['source'], sim_info['target'], 'peids')


    # Compute pe_deep_sim on all files of type pe
    results = c.batch_work_request('pe_deep_sim', {'type_tag': 'pe'})

    # Store the ssdeep sims as relationships
    for result in list(results):
        for sim_info in result['sim_list']:
            c.add_rel(result['md5'], sim_info['md5'], 'ssdeep')



def test():
    ''' pe_sim_graph test '''
    main()

if __name__ == '__main__':
    main()