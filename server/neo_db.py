
''' NeoDB class for WorkBench '''
import hashlib
import StringIO

class NeoDB():

    def __init__(self, uri='http://localhost:7474/db/data'):

        # Get connection to Neo4j
        try:
            self.graph_db = neo4j.GraphDatabaseService(uri)
            print 'Neo4j GraphDB connected: %s' % (str(uri))
        except:
            print 'Neo4j connection failed! Is your Neo4j server running?'
            exit(1)

    def add_node(self, md5, name, labels):
        ''' Add the node with name and labels '''
        node = self.graph_db.get_or_create_indexed_node('Node', 'md5', md5, {'md5':md5, 'name':name})
        node.add_labels(*labels)

    def has_node(self, md5):
        ''' Add the node with name and labels '''
        return True if self.graph_db.get_indexed_node('Node', 'md5', md5) else False

    def add_rel(self, source_md5, target_md5, rel):
        ''' Add a relationship: source, target must already exist (see add_node)
            'rel' is the name of the relationship 'contains' or whatever. '''

        # Add the relationship
        n1_ref = self.graph_db.get_indexed_node('Node', 'md5', source_md5)
        n2_ref = self.graph_db.get_indexed_node('Node', 'md5', target_md5)
        path = neo4j.Path(n1_ref, rel, n2_ref)
        path.get_or_create(self.graph_db)

class NeoDBStub():

    def __init__(self,  uri='http://localhost:7474/db/data'):
        print 'NeoDB Stub connected: %s' % (str(uri))
        print 'Install Neo4j and python bindings for Neo4j. See README.md'

    def add_node(self, md5, name, labels):
        print 'NeoDB Stub getting called...'

    def has_node(self, md5):
        print 'NeoDB Stub getting called...'

    def add_rel(self, source_md5, target_md5, rel):
        print 'NeoDB Stub getting called...'

try:
    from py2neo import neo4j
    NeoDB = NeoDB
except ImportError:
    NeoDB = NeoDBStub