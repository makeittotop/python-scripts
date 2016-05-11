from pymongo import MongoClient
import datetime

class QueueDb(object):
    def __init__(self, host='lic', port=27017):
        self._db = 'queue'
        self._collection = 'tasks'
        self._client = MongoClient('mongodb://{0}:{1}/'.format(host, port))

    def db(self):
        return self._db

    def collection(self):
        return self._collection

    def client(self):
        return self._client

    def insert(self, task_id, status='active'):
        db_obj = QueueDb()
        client = db_obj.client()
        # collection
        task_collection = client.queue.tasks

        task_doc = {}
        task_doc['task_id'] = task_id
        task_doc['sync_start'] = datetime.datetime.now()
        task_doc['status'] = status

    def update(self, task_id, status='done'):
        db_obj = QueueDb()
        client = db_obj.client()
        # collection
        task_collection = client.queue.tasks

        # Fetch a collection
        task_doc = task_collection.find_one({'task_id' : task_id})
        task_doc['sync_stop'] = datetime.datetime.now()
        task_doc['status'] = status

        # save
        task_collection.save(task_doc)


