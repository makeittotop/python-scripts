#!/usr/bin/env python

import sys
sys.path.append('/nas/projects/development/productionTools/py_queue/')

def queue_file_copy(src, dst=None, task_id=None):
    import queue_beta.tasks as t
    if not task_id:
        import uuid
        task_id = uuid.uuid4()
    
    if not dst:
        t.copy_file.apply_async((src, ), queue='hipri', task_id=str(task_id))
    else:
        t.copy_file.apply_async((src, dst), queue='hipri', task_id=str(task_id))
    print "Task successfully submitted with task id: " + str(task_id)
    return str(task_id)


def query_task_status(task_id):
    from celery.result import AsyncResult
    res = AsyncResult(task_id)

    return res.state

def query_task_status_block(task_id):
    from celery.result import AsyncResult
    res = AsyncResult(task_id)

    while not res.successful():
        if res.state.lower() == 'failure':
          print "Task {0} FAILED!".format(task_id)
          break

        import time
        time.sleep(0.3)
        print res.state

if __name__ == '__main__':
  task_id = queue_file_copy(['/nas/projects/development/productionTools/py_queue/tractordb-backup-2015-12-17.bakup', ]) 
  query_task_status_block(task_id)
