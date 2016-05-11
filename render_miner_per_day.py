#! /usr/bin/env python

class Job(object):
    def __init__(self):
        pass
    #1
    @property
    def jid(self):
        return self._jid 

    @jid.setter
    def jid(self, jid):
        self._jid = jid

    #2
    @property
    def owner(self):
        return self._owner 

    @owner.setter
    def owner(self, owner):
        self._owner = owner

    #3
    @property
    def meta_data(self):
        return self._meta_data

    @meta_data.setter
    def meta_data(self, meta_data):
        self._meta_data = meta_data

    #4
    @property
    def max_cid(self):
        return self._max_cid 

    @max_cid.setter
    def max_cid(self, max_cid):
        self._max_cid = max_cid 

    #5
    @property
    def first_task(self):
        return self._first_task 

    @first_task.setter
    def first_task(self, first_task):
        self._first_task = first_task

    #6
    @property
    def last_task(self):
        return self._last_task 

    @last_task.setter
    def last_task(self, last_task):
        self._last_task = last_task

    #7
    @property
    def title(self):
        return self._title 

    @title.setter
    def title(self, title):
        self._title = title

    #8
    @property
    def spool_time(self):
        return self._spool_time 

    @spool_time.setter
    def spool_time(self, spool_time):
        self._spool_time = spool_time

    #9
    @property
    def start_time(self):
        return self._start_time 

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    #10
    @property
    def stop_time(self):
        return self._stop_time 

    @stop_time.setter
    def stop_time(self, stop_time):
        self._stop_time = stop_time

    #11
    @property
    def pause_time(self):
        return self._pause_time 

    @pause_time.setter
    def pause_time(self, pause_time):
        self._pause_time = pause_time

    #12
    @property
    def num_tasks(self):
        return self._num_tasks

    @num_tasks.setter
    def num_tasks(self, num_tasks):
        self._num_tasks = num_tasks

    #13
    @property
    def num_blocked(self):
        return self._num_blocked 

    @num_blocked.setter
    def num_blocked(self, num_blocked):
        self._num_blocked = num_blocked

    #14
    @property
    def num_active(self):
        return self._num_active 

    @num_active.setter
    def num_active(self, num_active):
        self._num_active = num_active

    #15
    @property
    def num_ready(self):
        return self._num_ready 

    @num_ready.setter
    def num_ready(self, num_ready):
        self._num_ready = num_ready

    #16
    @property
    def num_error(self):
        return self._num_error 

    @num_error.setter
    def num_error(self, num_error):
        self._num_error = num_error

    #17
    @property
    def num_done(self):
        return self._num_done

    @num_done.setter
    def num_done(self, num_done):
        self._num_done = num_done

    #18
    @property
    def status(self):
        return self._status 

    @status.setter
    def status(self, status):
        self._status = status

    #19
    @property
    def elapsed_secs(self):
        return self._elapsed_secs 

    @elapsed_secs.setter
    def elapsed_secs(self, elapsed_secs):
        self._elapsed_secs = elapsed_secs
        
    #20    
    @property
    def tasks(self):
        return self._tasks
     
    @tasks.setter
    def tasks(self, tasks):
        self._tasks = tasks        

    def __repr__(self):
        return "#{0}: {1}#".format(self.jid, self.title)
        
class Task(object):
    def __init__(self):
        pass
    #1
    @property
    def jid(self):
        return self._jid

    @jid.setter
    def jid(self, jid):
        self._jid =  jid
    #2
    @property
    def tid(self):
        return self._tid

    @tid.setter
    def tid(self, tid):
        self._tid = tid
    #3
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
    #4
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
    #5    
    @property
    def active_time(self):
        return self._active_time

    @active_time.setter
    def active_time(self, active_time):
        self._active_time = active_time 
    #6
    @property
    def state_time(self):
        return self._state_time

    @state_time.setter
    def state_time(self, state_time):
        self._state_time = state_time
    #7    
    @property
    def ready_time(self):
        return self._ready_time

    @ready_time.setter
    def ready_time(self, ready_time):
        self._ready_time = ready_time 
    #8
    @property
    def progress(self):
        return self._progress
  
    @progress.setter
    def progress(self, progress):
        self._progress = progress        
    #9                                   
    @property
    def retry_count(self):
        return self._retry_count
    
    @retry_count.setter
    def retry_count(self, retry_count):
        self._retry_count = retry_count        
                                       
    def __repr__(self):
        #return "{0}".format(self.tid)
        return "#{0}:{1} - {2}#".format(self.jid, self.tid, self.title)

    def __str__(self):
        return repr(self)
                
class Invocation(object):
    def __init__(self):
        pass
  
    #1
    @property
    def blade(self):
        return self._blade

    @blade.setter
    def blade(self, blade):
        self._blade = blade

    #2
    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    #3
    @property
    def stop_time(self):
        return self._stop_time

    @stop_time.setter
    def stop_time(self, stop_time):
        self._stop_time = stop_time

    #4
    @property
    def retry_count(self):
        return self._retry_count

    @retry_count.setter
    def retry_count(self, retry_count):
        self._retry_count = retry_count

    #5
    @property
    def elapsed_app(self):
        return self._elapsed_app

    @elapsed_app.setter
    def elapsed_app(self, elapsed_app):
        self._elapsed_app = elapsed_app

    #6
    @property
    def elapsed_sys(self):
        return self._elapsed_sys

    @elapsed_sys.setter
    def elapsed_sys(self, elapsed_sys):
        self._elapsed_sys = elapsed_sys

    #7
    @property
    def elapsed_real(self):
        return self._elapsed_real

    @elapsed_real.setter
    def elapsed_real(self, elapsed_real):
        self._elapsed_real = elapsed_real

    #8
    @property
    def rcode(self):
        return self._rcode

    @rcode.setter
    def rcode(self, rcode):
        self._rcode = rcode

class Meta_Data(object) :
    def __init__(self, data_str):
        try:
            items = data_str.split("_")
        except ValueError:
            pass

        #print(data_str)

        try:
            self.seq = items[0]
            self.scn = items[1]
            self.shot = items[2]
            self.elem = items[3]
            self.dept = items[4]
            self.ver = items[5]
        except Exception:
            self.seq = 'N/A' #items[0]
            self.scn = 'N/A' #items[1]
            self.shot = 'N/A' #items[2]
            self.elem = 'N/A'
            self.dept = 'N/A'
            self.ver = 'N/A'
    
    @property
    def seq(self):
        return self._seq 

    
    @seq.setter
    def seq(self, seq):
        self._seq = seq

    
    @property
    def scn(self):
        return self._scn 

    
    @scn.setter
    def scn(self, scn):
        self._scn = scn

    
    @property
    def shot(self):
        return self._shot 

    
    @shot.setter
    def shot(self, shot):
        self._shot = shot

    
    @property
    def elem(self):
        return self._elem

    
    @elem.setter
    def elem(self, elem):
        self._elem = elem

    
    @property
    def dept(self):
        return self._dept 

    
    @dept.setter
    def dept(self, dept):
        self._dept = dept

    
    @property
    def ver(self):
        return self._ver 

    
    @ver.setter
    def ver(self, ver):
        self._ver = ver
        
# Standard
import datetime
import re
import csv
import sys
import argparse
import calendar

# Studio
import render.data.query as rquery

def get_jobs(start, stop):
    # Query string
    #date_str = datetime.date.strftime(date_arg, "%Y-%m-%d")
    query_str = "spooltime > '{0}' and spooltime < '{1}'".format(start, stop)

    jobs = []
    # Execute the query, for now we will query all jobs launched since the beginning of the day
    job_data = rquery.jobs(query_str, sortby=['jid'], archive=True)
    for data in job_data:
        jobs.append(get_job(data))

    return jobs

def get_job(data):
    meta_data = Meta_Data(data['title'])

    job = Job()

    job.jid = data['jid']
    job.owner = data['owner']
    job.max_cid= data['maxcid']
    job.title = data['title']
    job.spool_time = data['spooltime']
    job.start_time = data['starttime']
    job.stop_time = data['stoptime']
    job.pause_time = data['pausetime']
    job.elapsed_secs = data['elapsedsecs']
    job.num_tasks = data['numtasks']
    job.num_blocked = data['numblocked']
    job.num_ready = data['numready']
    job.num_active = data['numactive']
    job.num_error = data['numerror']
    job.num_done = data['numdone']
    job.meta_data = meta_data

    return job

def get_tasks(job):
    # Query string
    query_str = "jid = {0}".format(job.jid)

    tasks = []
    # Execute the query
    task_data = rquery.tasks(query_str, sortby = ['tid'], archive=True)
    for data in task_data:
        tasks.append(get_task(data))

    return tasks    

def get_task(data):
    task = Task()
    
    task.jid = data['jid']
    task.tid = data['tid']

    task.title = data['title']

    task.state = data['state']
    task.state_time = data['statetime']
    task.ready_time = data['readytime']
    task.active_time = data['activetime']
    task.progress = data['progress']
    task.retry_count = data['retrycount']

    return task

def write_to_csv(start_str, jobs):
    print >>sys.stderr, "Mining render data for {0}.".format(start_str)

    cvs_file = '/home/abhishek/dev/python/tractor_data_{0}.csv'.format(start_str)
    with open(cvs_file, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')

        '''
        data = [
                    ['Employee No','Employee Name','Job Desription','Salary'],
                    ['123453','Jack','CEO','12000'], 
                    ['453124','Jane','Director','25000'],
                    ['4568354','Sally','Marketing','68000'],
                    ['684535','Harry','Sales','56000'],
                ]
        

        for item in data:
            spamwriter.writerow(item)    
        '''
        
        row_header = [
                          "Number", 'jid', 'owner', 'seq', 'scn', 'shot', 'dept', 'version',
                          'title', 'first_task', 'last_task', 'spool_time', 'start_time',
                          'stop_time', 'pause_time','num_tasks', 'num_done', 'num_ready',
                          'num_error', 'num_active', 'num_blocked', 'elapsed_secs',
                          'tid', 'title', 'state', 'ready_time', 
                          'active_time', 'state_time', 'retry_count'                          
                      ]
        csvwriter.writerow(row_header)

        count = 1
        for job in jobs:
            row_data = [
                           count, job.jid, job.owner, job.meta_data.seq, job.meta_data.scn, job.meta_data.shot,
                           job.meta_data.dept, job.meta_data.ver, job.title, job.first_task, job.last_task, 
                           job.spool_time, job.start_time, job.stop_time, job.pause_time,
                           job.num_tasks, job.num_done, job.num_ready, job.num_error, job.num_active,
                           job.num_blocked, job.elapsed_secs,
                       ]
            csvwriter.writerow(row_data)

            '''
            row_header = [
                            'tid', 'title', 'state', 'ready_time', 
                            'active_time', 'state_time', 'retry_count'
                         ]
            csvwriter.writerow(row_header)
            '''

            for task in job.tasks:
                row_data = [
                               '', '', '', '', '', '', '', 
                               '', '', '', '', '', '',
                               '', '', '', '', '', '',
                               '', '', '',
                               task.tid, task.title, task.state,
                               task.ready_time, task.active_time, 
                               task.state_time, task.retry_count
                           ]

                csvwriter.writerow(row_data)         
            
            empty_data = [
                               '', '', '', '', '', '', '', 
                               '', '', '', '', '', '',
                               '', '', '', '', '', '',
                               '', '', '', '', '', '',
                               '', '', '',
                         ]
            csvwriter.writerow(empty_data)  
            count += 1  

def split_args(value):
    values = value.split()

    if len(values) > 2:
        raise argparse.ArgumentError

    return values

        
def arg_parse():
    parser = argparse.ArgumentParser(description='This is a Tractor render data mining program', prefix_chars = "@")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("@t", "@@time", action="store", type=split_args, dest='time')
    group.add_argument("@d", "@@date", action="store", type=split_args, dest='date')

    print(parser.parse_args())
    sys.exit(0)

def main():
    #arg_parse()
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])

    month_range = calendar.monthrange(year, month)[1]

    rquery.setEngineClientParam(hostname="fox", port=1503)

    print >>sys.stderr, ">>>>Start"

    for i in xrange(day, month_range + 1):
        start = datetime.datetime(year, month, i)
        if start > datetime.datetime.today():
            break

        stop = datetime.datetime(year, month, i, 23, 59, 59)

        jobs = get_jobs(start, stop)
        if not jobs:
            continue
             
        for job in jobs:
            job.tasks = get_tasks(job)
            for task in job.tasks:
                if 'Renders' in task.title:
                    (first_task_str, last_task_str) = task.title.split()[1].split('-')
                    job.first_task = int(first_task_str)
                    job.last_task = int(last_task_str)
                    break
                else:
                    job.first_task = 0 #'N/A'
                    job.last_task = 0 #'N/A'
                    break

        write_to_csv(start.strftime("%Y-%m-%d"), jobs)

    print >>sys.stderr, ">>>>Stop"

if __name__ == '__main__':
    main()
