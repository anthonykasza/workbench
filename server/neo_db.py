
''' NeoDB class for WorkBench '''

class NeoDB():

    def __init__(self, uri='http://localhost:7474/db/data'):

        # Get connection to Neo4j
        try:
            # Open the Neo4j DB and get version (just testing Neo connection)
            self.graph_db = neo4j.GraphDatabaseService(uri)
            version = self.graph_db.neo4j_version
            print 'Neo4j GraphDB connected: %s %s' % (str(uri), version)
        except packages.httpstream.http.SocketError:
            print 'Neo4j connection failed! Is your Neo4j server running? $ neo4j start'
            raise RuntimeError('Could not connect to Neo4j')

    def add_node(self, node_id, name, labels):
        ''' Add the node with name and labels '''
        node = self.graph_db.get_or_create_indexed_node('Node', 'node_id', node_id, {'node_id':node_id, 'name':name})
        try:
            node.add_labels(*labels)
        except NotImplementedError:
            print 'Got a NotImplementedError when adding labels. Upgrade your Neo4j DB!'

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
        self.graph_db.clear()

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
    from py2neo import packages
    NeoDB = NeoDB
except (ImportError, RuntimeError):
    NeoDB = NeoDBStub
