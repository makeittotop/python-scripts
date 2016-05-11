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



