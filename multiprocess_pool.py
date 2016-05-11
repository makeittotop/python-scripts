#!/usr/bin/env python

import multiprocessing
import time
import sys
import redis

class Consumer(multiprocessing.Process):
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue

    def run(self):
        proc_name = self.name
        while True:
            print >>sys.stderr, "[{0}] Awaiting next task...".format(proc_name)

            next_task = self.task_queue.get()

            print >>sys.stderr, "[{0}] Got task... {1}".format(proc_name, next_task)

            if next_task is None:
                # Poison pill means shutdown
                print >>sys.stderr, '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break

            print>>sys.stderr, '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
        return


class Task(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self):
        time.sleep(10) # pretend to take some time to do the work
        return '%s * %s = %s' % (self.a, self.b, self.a * self.b)
    def __str__(self):
        return '%s * %s' % (self.a, self.b)


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() / 2
    print >>sys.stderr, 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()

    try:
        r_server = redis.Redis("lic", port=4444, db=1)
        pubsub = r_server.pubsub()
        pubsub.subscribe("djv")
    except Exception as e:
        print e.message
        sys.exit(0)

    # Enqueue jobs
    for i in pubsub.listen():
        print i['channel'], ":", i['data']

    num_jobs = 10
    for i in xrange(num_jobs):
        tasks.put(Task(i, i))

    # Wait for all of the tasks to finish
    tasks.join()


"""
import multiprocessing as mp
import time

def foo_pool(x):
    time.sleep(2)
    return x*x

result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def apply_async_with_callback():
    pool = mp.Pool()
    for i in range(10):
        pool.apply_async(foo_pool, args = (i, ), callback = log_result)
    pool.close()
    pool.join()
    print(result_list)

if __name__ == '__main__':
    apply_async_with_callback()

import os, sys, time

from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing

def test_func(i):
    while True:
        print ("Number # {0}".format(i))
        print "Sleeping for 5 secs"
        time.sleep(5)


print 'cpu_count() = %d\n' % multiprocessing.cpu_count()

pool = ThreadPool(5)
for i in range(5):
    pool.apply_async(test_func, [i])

pool.close()
pool.join()


import multiprocessing
import time

# consumer
class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        print "{0} ready...".format(proc_name)

        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return

# worker - called by the consumer
class Task(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self):
        time.sleep(5) # pretend to take some time to do the work
        return '%s * %s = %s' % (self.a, self.b, self.a * self.b)
    def __str__(self):
        return '%s * %s' % (self.a, self.b)


# producer
if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks, results)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 25
    for i in xrange(num_jobs):
        tasks.put(Task(i, i))

    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)


    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result:', result
        num_jobs -= 1
"""





