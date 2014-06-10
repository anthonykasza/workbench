
''' ELS_Indexer class for WorkBench '''

class ELS_Indexer():

    def __init__(self, hosts=[{"host": "localhost", "port": 9200}]):

        # Get connection to ElasticSearch
        try:
            self.es = elasticsearch.Elasticsearch(hosts)
            info = self.es.info()
            version = info['version']
            print 'ELS Indexer connected: %s %s %s %s' % (str(hosts), info['name'], version['number'], version['lucene_version'])
        except:
            print 'ELS connection failed! Is your ELS server running?'
            exit(1)

    def index_data(self, data, index_name='meta', doc_type='unknown'):

        # Index the data (which needs to be a dict/object) if it's not
        # we're going to toss an exception
        if not isinstance(data, dict):
            raise RuntimeError('Index failed, data needs to be a dict!')

        try:
            self.es.index(index=index_name, doc_type=doc_type, body=data)
        except Exception, error:
            print 'Index failed: %s' % str(error)
            raise RuntimeError('Index failed: %s' % str(error))

    def search(self, index_name, query):
        try:
            results = self.es.search(index=index_name, body=query)
            return results
        except Exception, error:
            error_str = 'Query failed: %s\n' % str(error)
            error_str += '\nVersion 1.2+ has dynamic scripting disabled, see %s' % \
                  ('http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html#_enabling_dynamic_scripting')
            print error_str
            raise RuntimeError(error_str)

class ELS_StubIndexer():

    def __init__(self, hosts=[{"host": "localhost", "port": 9200}]):
        print 'ELS Stub Indexer connected: %s' % (str(hosts))
        print 'Install ElasticSearch and python bindings for ELS indexer. See README.md'

    def index_data(self, data, index_name='meta', doc_type='unknown'):
        print 'ELS Stub Indexer getting called...'

    def search(self, index_name, query):
        print 'ELS Stub Indexer getting called...'

try:
    import elasticsearch
    ELS_Indexer = ELS_Indexer
except ImportError:
    ELS_Indexer = ELS_StubIndexer
