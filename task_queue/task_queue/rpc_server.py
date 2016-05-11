#!/usr/bin/env python

import zerorpc
import pymongo
from celery import Celery
 
client = pymongo.MongoClient('localhost', 27017)
collection = client.queue.tasks

class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name

class Queue(object):
    def hello(self, name):
        return "Hello, %s" % name

    def set_task_status(self, type, task_id, status='cancelled'):
        if type == 'up':
            query_string = { 'upload_id' : task_id }
        elif type == 'down':
            query_string = { 'download_id' : task_id }

        task = collection.find_one(query_string)
        
        if type == 'up':
            task['upload_status'] = status
        elif type == 'down':
            task['download_status'] = status

        collection.save(task)

    def cancel_pending_task(self, type, task_id):
        app = Celery(broker="redis://localhost:4444/0")
        app.control.revoke(task_id, terminate=False)

        self.set_task_status(type.lower(), task_id)

        return True

    def cancel_running_task(self, type, task_id):
        app = Celery(broker="redis://localhost:4444/0")
        app.control.revoke(task_id, terminate=True)

        self.set_task_status(type.lower(), task_id)

        return True
        

#s = zerorpc.Server(HelloRPC())
s = zerorpc.Server(Queue())
s.bind("tcp://0.0.0.0:4242")
s.run()
