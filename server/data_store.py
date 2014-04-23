
''' DataStore class for WorkBench '''

import pymongo
import gridfs
import hashlib
import datetime
import bson


class DataStore():

    def __init__(self, uri='mongodb://localhost/workbench', database='workbench', capped=0):

        self.sample_collection = 'samples'
        self.capped = capped

        # Get connection to mongo
        self.uri = uri
        self.db_name = database
        self.c = pymongo.MongoClient('mongodb://'+self.uri+'/'+self.db_name)
        self.db = self.c.get_default_database()

        # Get the gridfs handle
        self.gridfs_handle = gridfs.GridFS(self.db)

        # Run the periodic operations
        self.periodic_ops()

        print 'WorkBench DataStore connected: %s' % (uri)

    def get_uri(self):
        return self.uri

    def store_sample(self, filename, sample_bytes, type_tag):

        sample_info = {}

        # Compute the MD5 hash
        sample_info['md5'] = hashlib.md5(sample_bytes).hexdigest()

        # Check if sample already exists
        sample = self.db[self.sample_collection].find_one({'md5':sample_info['md5']})
        if (sample):
            print 'Sample %s: already exists in DataStore' % (sample_info['md5'])
            return sample_info['md5']

        # Filename, length, import time and type_tag
        sample_info['filename'] = filename
        sample_info['length'] = len(sample_bytes)
        sample_info['import_time'] = datetime.datetime.utcnow()
        sample_info['type_tag'] = type_tag

        # Random customer for now
        import random
        sample_info['customer'] = random.choice(['Mega Corp','Huge Inc','BearTron','Dorseys Mom'])

        # Goes into the sample collection and GridFS

        # Push the file into the MongoDB GridFS
        print 'Storing Sample into Mongo GridFS'
        sample_info['__grid_fs'] = self.gridfs_handle.put(sample_bytes)
        self.db[self.sample_collection].insert(sample_info)

        return sample_info['md5']

    def clean_for_serialization(self, data):
        if isinstance(data, dict):
            for k in data.keys():
                if (k.startswith('__')): del data[k]
                elif isinstance(data[k], bson.objectid.ObjectId): del data[k]
                elif isinstance(data[k], datetime.datetime):
                    data[k] = data[k].isoformat()+'Z'
                elif isinstance(data[k], dict):
                    data[k] = self.clean_for_serialization(data[k])
                elif isinstance(data[k], list):
                    data[k] = [self.clean_for_serialization(item) for item in data[k]]
        return data

    def clean_for_storage(self, data):
        data = self.data_to_unicode(data)
        if isinstance(data, dict):
            for k in data.keys():
                if k == '_id':
                    del data[k]
                    continue
                if '.' in k:
                    new_k = k.replace('.', '_')
                    data[new_k] = data[k]
                    del data[k]
                    k = new_k
                if isinstance(data[k], dict):
                    data[k] = self.clean_for_storage(data[k])
                elif isinstance(data[k], list):
                    data[k] = [self.clean_for_storage(item) for item in data[k]]
        return data

    def get_sample(self, md5_or_filename):
        sample_info = self.db[self.sample_collection].find_one({'md5':md5_or_filename})
        if (not sample_info):
            sample_info = self.db[self.sample_collection].find_one({'filename':md5_or_filename})
            if (not sample_info):
                raise Exception('Sample %s not found in Data Store' % (md5_or_filename))
        grid_fs_id = sample_info['__grid_fs']
        sample_info = self.clean_for_serialization(sample_info)
        sample_info.update({'raw_bytes':self.gridfs_handle.get(grid_fs_id).read()})
        return sample_info

    def have_sample(self, md5_or_filename):
        # Try both md5 and filename
        info = self.db[self.sample_collection].find_one({'md5':md5_or_filename})
        if info: return info['md5']
        else:
            info = self.db[self.sample_collection].find_one({'filename':md5_or_filename})
            if info: return info['md5']
        return None

    def store_work_results(self, results, collection, md5):
        results['md5'] = md5
        results['__time_stamp'] = datetime.datetime.utcnow()

        # Fixme: Occasionally a capped collection will not let you update with a 
        #        larger object, if you have MongoDB 2.6 or above this shouldn't
        #        really happen, so for now just kinda punting and giving a message.
        try:
            self.db[collection].update({'md5':md5}, self.clean_for_storage(results), True)
        except pymongo.errors.OperationFailure:
            print 'Not updating exising object in capped collection...(upgrade to mongodb 2.6)'

    def get_work_results(self, collection, md5):
        return self.db[collection].find_one({'md5':md5})

    def all_sample_md5s(self, type_tag=None):
        if type_tag:
            cursor = self.db[self.sample_collection].find({'type_tag':type_tag},{'md5':1, '_id':0})
        else:
            cursor = self.db[self.sample_collection].find({},{'md5':1, '_id':0})
        return [ match.values()[0] for match in cursor]

    def periodic_ops(self):
        ''' Run periodic operations on the the data store
            Things like making sure collections are capped
            and indexes are set up '''

        # Get all the collections in the workbench database
        all_c = self.db.collection_names()
        all_c.remove('system.indexes')
        all_c.remove('fs.chunks')

        # Convert collections to capped if desired
        if (self.capped):
            size = self.capped * pow(1024, 2)  # self.capped MegaBytes per collection
            for collection in all_c:
                if collection == 'samples': # Samples collection get 10x allocation
                    self.db.command('convertToCapped', collection, size=size*10)
                else:
                    self.db.command('convertToCapped', collection, size=size)

        # Loop through all collections ensuring they have an index on MD5s
        for collection in all_c:
            self.db[collection].ensure_index('md5')

        # Add another index for filename on the samples collection
        self.db[self.sample_collection].ensure_index('filename')

    # Helper functions
    def to_unicode(self, s):

        # Fixme: This is total horseshit
        if isinstance(s, unicode):
            return s
        if isinstance(s, str):
            return unicode(s, errors='ignore')

        # Just return the original object
        return s

    def data_to_unicode(self, data):
        if isinstance(data, dict):
            return {self.to_unicode(k): self.to_unicode(v) for k, v in data.iteritems()}
        if isinstance(data, list):
            return [self.to_unicode(l) for l in data]
        else:
            return self.to_unicode(data)
