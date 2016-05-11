import time, pexpect, multiprocessing, threading, sys, re
from Queue import Queue

from celery import Celery, Task

from task_queue.mail import Mail
from task_queue.log import register_task_logger, get_or_create_task_logger
from task_queue.task_exception import TaskException

app = Celery('task_queue.tasks')
app.config_from_object('task_queue.celeryconfig')

@app.task
@register_task_logger(__name__)
class TestTask(Task):
    def run(self, x, y):
        try:
	    task_id = self.request.id

	    #logger = get_or_create_task_logger(func=add)
	    self.log.info("[%s]: add(%d, %d)" % (task_id, x, y))

	    result = x + y
	    self.log.info("[%s]: add(%d, %d) result: %d" % (task_id, x, y, result))
        except Exception as exc:
            self.retry(exc=exc, countdown=10)

	return result

    def on_success(self, retval, task_id, args, kwargs):
        self.log.info("[{0}]: SUCCESS : {1}".format(task_id, retval))

        # SEND DONE MAIL
        mail_obj = Mail(mail_type='UPLOAD_COMPLETE', task_id=task_id, retval=retval)        
        mail_obj.send()
        self.log.info("[{0}]: UPLOAD COMPLETE MAIL SENT".format(task_id))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.log.info("[{0}]: FAILURE : {1}".format(task_id, exc))

        # SEND FAIL MAIL
        mail_obj = Mail(mail_type='UPLOAD_FAIL', exc=exc, task_id=task_id, einfo=einfo)        
        mail_obj.send()
        self.log.info("[{0}]: UPLOAD FAIL MAIL SENT".format(task_id))

@app.task
@register_task_logger(__name__)
class SyncTask(Task):
    def run(self, dep_file_path, cmd):
        task_id = self.request.id
        #logger = get_or_create_task_logger(func=sync)

        # SEND SUBMIT MAIL
        mail_obj = Mail(mail_type='UPLOAD_SUBMIT', task_id=task_id)
        mail_obj.send()
        self.log.info("[{0}]: UPLOAD SUBMIT MAIL SENT".format(task_id))

        self.log.info("[{0}]: Dep file: {1}".format(task_id, dep_file_path))
        self.log.info("[{0}]: Start command: {1}".format(task_id, cmd))

        retval = self.exec_cmd(task_id, cmd)
        self.log.info("[{0}]: Finish command: {1}".format(task_id, cmd))
        if retval == 0:
            #msg = "[{0}]: Sync successful".format(task_id)
            #self.log.info(msg)
            return task_id
        else:
            # raise an error
            msg = "[{0}]: Sync failed: {0}".format(task_id)
            self.log.info(msg)
            raise TaskException(msg)
            '''
            try:
                msg = "[{0}]: Sync failed: {0}".format(task_id)
                self.log.info(msg)
                raise TaskException(msg)
            except TaskException as exc:
                pass
                #self.retry(exc=exc, countdown=5)
            '''

    def on_success(self, retval, task_id, args, kwargs):
        #self.log.info("[{0}]: SUCCESS : {1}".format(task_id, retval))

        # SEND DONE MAIL
        mail_obj = Mail(mail_type='UPLOAD_COMPLETE', task_id=task_id, retval=retval)        
        mail_obj.send()
        self.log.info("[{0}]: UPLOAD COMPLETE MAIL SENT".format(task_id))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        #self.log.info("[{0}]: FAILURE : {1}".format(task_id, exc))

        # SEND FAIL MAIL
        mail_obj = Mail(mail_type='UPLOAD_FAIL', exc=exc, task_id=task_id, einfo=einfo)        
        mail_obj.send()
        self.log.info("[{0}]: UPLOAD FAIL MAIL SENT".format(task_id))

    def exec_cmd(self, task_id, cmd):
        thread = pexpect.spawn(cmd)

        self.log.info("[[{0}]: (thread) START]".format(task_id))

        cpl = thread.compile_pattern_list([pexpect.EOF,
						   '(.*)'])
        self.error_count = 0
        while True:
            i = thread.expect_list(cpl, timeout=None)
	    if i == 0: # EOF
	        self.log.info("[[{0}]: (thread) STOP]".format(task_id))
	        break
	    elif i == 1:
	        progress_output = thread.match.group(1)
                progress_output = progress_output.strip()

		self.log.info("[{0}]: {1}".format(task_id, progress_output))

	        #We need to mine data for errors very carefully.
	        #In case there is an error, we need to keep the task going to completion
	        #But make sure that the 'CHAIN' shouldn't propogate further i.e. 'RENDER'
		#threads mustn't launch
                if re.match(r'.*error.*', progress_output, flags=re.IGNORECASE & re.MULTILINE):
                    self.log.info("[{0}]: Detected an error in the transfer stream: {1}".format(task_id, progress_output))
                    self.error_count += 1 

	thread.close()

        if not self.error_count:
            return 0
        else:
            return -1

    def send_mail(**kwargs):
        mail_obj = Mail(**kwargs)        
        mail_obj.send()
        self.log.info("[{0}]: UPLOAD FAIL MAIL SENT".format(task_id))
         
@app.task
@register_task_logger(__name__)
class DownloadTask(Task):
    def run(self, dep_file_path, cmd):
        task_id = self.request.id
        #logger = get_or_create_task_logger(func=sync)

        # SEND SUBMIT MAIL
        mail_obj = Mail(mail_type='DOWNLOAD_SUBMIT', task_id=task_id)
        mail_obj.send()
        self.log.info("[{0}]: DOWNLOAD SUBMIT MAIL SENT".format(task_id))

        self.log.info("[{0}]: Dep file: {1}".format(task_id, dep_file_path))
        self.log.info("[{0}]: Start command: {1}".format(task_id, cmd))

        retval = self.exec_cmd(task_id, cmd)
        self.log.info("[{0}]: Finish command: {1}".format(task_id, cmd))
        if retval == 0:
            #msg = "[{0}]: Sync successful".format(task_id)
            #self.log.info(msg)
            return task_id
        else:
            # raise an error
            msg = "[{0}]: Download failed: {0}".format(task_id)
            self.log.info(msg)
            raise TaskException(msg)
            '''
            try:
                msg = "[{0}]: Sync failed: {0}".format(task_id)
                self.log.info(msg)
                raise TaskException(msg)
            except TaskException as exc:
                pass
                #self.retry(exc=exc, countdown=5)
            '''

    def on_success(self, retval, task_id, args, kwargs):
        #self.log.info("[{0}]: SUCCESS : {1}".format(task_id, retval))

        # SEND DONE MAIL
        mail_obj = Mail(mail_type='DOWNLOAD_COMPLETE', task_id=task_id, retval=retval)        
        mail_obj.send()
        self.log.info("[{0}]: DOWNLOAD COMPLETE MAIL SENT".format(task_id))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        #self.log.info("[{0}]: FAILURE : {1}".format(task_id, exc))

        # SEND FAIL MAIL
        mail_obj = Mail(mail_type='DOWNLOAD_FAIL', exc=exc, task_id=task_id, einfo=einfo)        
        mail_obj.send()
        self.log.info("[{0}]: DOWNLOAD FAIL MAIL SENT".format(task_id))

    def exec_cmd(self, task_id, cmd):
        thread = pexpect.spawn(cmd)

        self.log.info("[[{0}]: (thread) START]".format(task_id))

        cpl = thread.compile_pattern_list([pexpect.EOF,
						   '(.*)'])
        self.error_count = 0
        while True:
            i = thread.expect_list(cpl, timeout=None)
	    if i == 0: # EOF
	        self.log.info("[[{0}]: (thread) STOP]".format(task_id))
	        break
	    elif i == 1:
	        progress_output = thread.match.group(1)
                progress_output = progress_output.strip()

		self.log.info("[{0}]: {1}".format(task_id, progress_output))

	        #We need to mine data for errors very carefully.
	        #In case there is an error, we need to keep the task going to completion
	        #But make sure that the 'CHAIN' shouldn't propogate further i.e. 'RENDER'
		#threads mustn't launch
                if re.match(r'.*error.*', progress_output, flags=re.IGNORECASE & re.MULTILINE):
                    self.log.info("[{0}]: Detected an error in the transfer stream: {1}".format(task_id, progress_output))
                    self.error_count += 1 

	thread.close()

        if not self.error_count:
            return 0
        else:
            return -1

    def send_mail(**kwargs):
        mail_obj = Mail(**kwargs)        
        mail_obj.send()
        self.log.info("[{0}]: DOWNLOAD FAIL MAIL SENT".format(task_id))

@app.task
@register_task_logger(__name__)
class SpoolTask(Task):
    def run(self, engine, priority, alf_script):
        task_id = self.request.id
        cmd = "task_queue.rfm.tractor.Spool(['--engine={0}', '--priority={1}', '{2}'])".format(engine, priority, alf_script)
        self.log.info("[{0}]: Start command: {1}".format(task_id, cmd))

        # Execute `cmd`
        import task_queue.rfm.tractor
        import json
        ret_val = task_queue.rfm.tractor.Spool(['--engine={0}'.format(engine), '--priority={0}'.format(priority), '{0}'.format(alf_script)])
        self.log.info("[{0}]: Finish command: {1}".format(task_id, cmd))
        return json.loads(ret_val).get('jid')

    def on_success(self, retval, task_id, args, kwargs):
        # SEND SPOOL COMPLETE MAIL
        mail_obj = Mail(mail_type='SPOOL_COMPLETE', task_id=task_id, retval=retval)
        mail_obj.send()
        self.log.info("[{0}]: SPOOL COMPLETE MAIL SENT".format(task_id))

        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


"""
def logger_func(logger, msg):
    logger.info(msg)
    #print >>sys.stderr, msg

def exec_cmd(task_id, cmd, logger):
    thread = pexpect.spawn(cmd)

    logger_func(logger, "[[{0}]: (thread) START]".format(task_id))

    cpl = thread.compile_pattern_list([pexpect.EOF,
                                           '(.*)'])
    while True:
        i = thread.expect_list(cpl, timeout=None)
        if i == 0: # EOF
            logger_func(logger, "[[{0}]: (thread) STOP]".format(task_id))
            break
        elif i == 1:
            progress_output = thread.match.group(1)
            #We need to mine data for errors very carefully.
            #In case there is an error, we need to keep the task going to completion
            #But make sure that the 'CHAIN' shouldn't propogate further i.e. 'RENDER'
            #threads mustn't launch
            logger_func(logger, "[{0}]: {1}".format(task_id, progress_output.strip()))
    thread.close()

    return 1

@app.task
def sync(dep_file_path, cmd):
    task_id = sync.request.id
    logger = get_or_create_task_logger(func=sync)

    logger_func(logger, "[{0}]: Dep file: {1}".format(task_id, dep_file_path))
    logger_func(logger, "[{0}]: Start command: {1}".format(task_id, cmd))

    success = exec_cmd(task_id, cmd, logger)

    logger_func(logger, "[{0}]: Finish command: {1}".format(task_id, cmd))

    if success:
        msg = "[{0}]: Sync successful".format(task_id)
        logger_func(logger, msg)

        return msg
    else:
        # raise an error
	msg = "[{0}]: Sync failed".format(task_id)
        logger_func(logger, msg)

    pass

@app.task
def render():
    pass

@app.task
def fetch():
    pass


'''
def add_worker(in_q):
    print threading.currentThread().getName(), 'Starting'
    for i in xrange(100):
        in_q.put("Sleeping for: {0} time(s)".format(i + 1))
        #print("Sleeping for: {0} time".format(i + 1))
        time.sleep(1)
    print threading.currentThread().getName(), 'Stoping'
    return

def mult_worker():
    print multiprocessing.current_process().name, 'Starting'
    time.sleep(200)
    print multiprocessing.current_process().name, 'Stoping'
    return

'''

@app.task
def add(x, y):
    task_id = add.request.id
    logger = get_or_create_task_logger(func=add)
    logger_func(logger, "[%s]: add(%d, %d)" % (task_id, x, y))

    '''
    q = Queue()

    t = threading.Thread(target=add_worker, name="add_worker", args=(q,)) 
    logger_func(logger, "New thread starting")
    t.start()

    while t.is_alive():
        print("From the Main-thread: ", q.get())

    t.join()
    logger_func(logger, "New thread finishing")
    '''

    result = x + y
    logger_func(logger, "Returning add(%d, %d) result: %d" % (x, y, result))
    return result

@app.task
def mult(x, y):
    logger = get_or_create_task_logger(func=mult)
    logger_func(logger, "Calling task mult(%d, %d)" % (x, y))

    '''
    p = multiprocessing.Process(target=mult_worker, name="mult_worker") 
    p.start()
    p.join()
    '''

    return x * y
"""
