import zerorpc
import argparse
import os
import pprint

def main():


    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=4242, help='port used by workbench server')
    args = parser.parse_args()
    port = str(args.port)
    c = zerorpc.Client()
    c.connect('tcp://127.0.0.1:'+port)

    # Test out PEFile -> strings -> indexer -> search
    file_list = [os.path.join('../data/pe/bad', child) for child in os.listdir('../data/pe/bad')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'pe')

            # Index the strings and features output (notice we can ask for any worker output)
            # Also (super important) it all happens on the server side.
            c.index_worker_output('strings', md5, 'strings', None)
            print '\n<<< Strings for PE: %s Indexed>>>' % (filename)
            c.index_worker_output('pe_features', md5, 'pe_features', None)
            print '<<< Features for PE: %s Indexed>>>' % (filename)

    # Well we should execute some queries against ElasticSearch at this point but as of
    # version 1.2+ the dynamic scripting disabled by default, see
    # 'http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html#_enabling_dynamic_scripting

    '''
    # Now actually do something interesing with our ELS index
    # ES Facets are kewl (http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-facets.html)
    facet_query = '{"facets" : {"tag" : {"terms" : {"field" : "string_list","script": "term.length() > 3 ? true: false"}}}}'
    results = c.search('strings',facet_query)
    try:
        print '\nQuery: %s' % facet_query
        print 'Number of hits: %d' % results['hits']['total']
        print 'Max Score: %f' % results['hits']['max_score']
        pprint.pprint(results['facets'])
    except TypeError:
        print 'Probably using a Stub Indexer, if you want an ELS Indexer see the readme'


    # Fuzzy is kewl (http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html)
    fuzzy_query = '{"fields":["md5","sparse_features.imported_symbols"],"query": {"fuzzy" : {"sparse_features.imported_symbols" : "loadlibrary"}}}'
    results = c.search('pe_features',fuzzy_query)
    try:
        print '\nQuery: %s' % fuzzy_query
        print 'Number of hits: %d' % results['hits']['total']
        print 'Max Score: %f' % results['hits']['max_score']
        pprint.pprint([ (hit['fields']['md5'], hit['fields']['sparse_features.imported_symbols']) for hit in results['hits']['hits'] ])
    except TypeError:
        print 'Probably using a Stub Indexer, if you want an ELS Indexer see the readme'
    '''


def test():
    ''' pe_strings_indexer test '''
    main()

if __name__ == '__main__':
    main()
