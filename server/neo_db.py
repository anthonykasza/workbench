
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

    def add_node(self, node_id, name, labels):
        ''' Add the node with name and labels '''
        node = self.graph_db.get_or_create_indexed_node('Node', 'node_id', node_id, {'node_id':node_id, 'name':name})
        node.add_labels(*labels)

    def has_node(self, node_id):
        ''' Add the node with name and labels '''
        return True if self.graph_db.get_indexed_node('Node', 'node_id', node_id) else False

    def add_rel(self, source_node_id, target_node_id, rel):
        ''' Add a relationship: source, target must already exist (see add_node)
            'rel' is the name of the relationship 'contains' or whatever. '''

        # Add the relationship
        n1_ref = self.graph_db.get_indexed_node('Node', 'node_id', source_node_id)
        n2_ref = self.graph_db.get_indexed_node('Node', 'node_id', target_node_id)

        # Sanity check
        if not n1_ref or not n2_ref:
            print 'Cannot add relationship between unfound nodes: %s --> %s' % (source_node_id, target_node_id)
            return
        path = neo4j.Path(n1_ref, rel, n2_ref)
        path.get_or_create(self.graph_db)

    def clear_db(self):
        ''' Clear the Graph Database of all nodes and edges '''
        query = neo4j.CypherQuery(self.graph_db, 'match (n)-[r]-() delete n,r')
        query.run()
        query = neo4j.CypherQuery(self.graph_db, 'match n delete n')
        query.run()

class NeoDBStub():

    def __init__(self,  uri='http://localhost:7474/db/data'):
        print 'NeoDB Stub connected: %s' % (str(uri))
        print 'Install Neo4j and python bindings for Neo4j. See README.md'

    def add_node(self, node_id, name, labels):
        print 'NeoDB Stub getting called...'

    def has_node(self, node_id):
        print 'NeoDB Stub getting called...'

    def add_rel(self, source_node_id, target_node_id, rel):
        print 'NeoDB Stub getting called...'

    def clear_db(self):
        print 'NeoDB Stub getting called...'

try:
    from py2neo import neo4j
    NeoDB = NeoDB
except ImportError:
    NeoDB = NeoDBStub
