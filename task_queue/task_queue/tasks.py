import time, pexpect, multiprocessing, threading, sys, re, datetime
import random
from Queue import Queue
from celery import Celery, Task

from task_queue.mail import Mail
from task_queue.log import register_task_logger, get_or_create_task_logger
from task_queue.task_exception import TaskException
from task_queue.db import QueueDb

import tractor.api.query as tq


app = Celery('task_queue.tasks')
app.config_from_object('task_queue.celeryconfig')

QUE_SUBMIT_BIN = 'bin/submit_to_queue.py'
FIX_MAYA_FILE_BIN = "/nas/projects/development/productionTools/pipeline.config/fix_maya_version.py"

@app.task
@register_task_logger(__name__)
class UploadTestTask(Task):
    max_retries = 3
    default_retry_delay = 3

    def exec_cmd(self, task_id, cmd):
        thread = pexpect.spawn(cmd)

        self.log.info("[[{0}]: (thread) START]".format(task_id))

        cpl = thread.compile_pattern_list([pexpect.EOF,
						   '(.*)'])
        self.error_count = 0
        self.errors = []
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
                po_words = map(lambda x: x.lower(), progress_output.split('\s'))

                error_po_words = filter(lambda x: 'error' in x, po_words)
                if not error_po_words:
                    continue

                user_po_words = filter(lambda x: 'user' in x, po_words)
                if user_po_words:
                    self.log.info("[{0}]: Detected a user kill signal in the transfer stream, aborting: {1}".format(task_id, progress_output))
                    self.error_count += 1
                    self.errors.append(progress_output)
                    self.error_type='user_abort'
                    break

                if error_po_words:
                    self.log.info("[{0}]: Detected a critical error in the transfer stream, aborting: {1}".format(task_id, progress_output))
                    self.error_count += 1
                    self.errors.append(progress_output)
                    self.error_type='critical_error'
                    break

                '''
                for word in po_words:
                    if 'eagain' in word:
                #if re.match(r'.*error.*', progress_output, flags=re.IGNORECASE):
                    #if re.match(r'.*eagain.*', progress_output, flags=re.IGNORECASE):
                        # Session Stop  (Error: Session shutdown failed, Tried to write different output after EAGAIN)
                        self.log.info("[{0}]: Detected a CRITICAL error in the transfer stream, aborting: {1}".format(task_id, progress_output))
			self.error_count += 1
			self.errors.append(progress_output)
                        self.should_retry=True
                        break
                    elif 'user' in word:
                        self.log.info("[{0}]: Detected an error in the transfer stream: {1}".format(task_id, progress_output))
			self.error_count += 1
			self.errors.append(progress_output)
                        self.should_retry=False
                        break
                '''
	thread.close()

        if not self.error_count:
            return 0
        else:
            raise TaskException(self.errors[0])

    def run(self, task_owner, dep_file_path, cmd, task_uuid, unique_id, alf_script, operation, count, **kwargs):
        task_id = self.request.id
        self.task_uuid = task_uuid

        self.error_type = None

        self.task_owner = task_owner
        self.dep_file_path = dep_file_path
        self.unique_id = unique_id
        self.alf_script = alf_script
        self.operation = operation

        # First try 
        if count == 0:
            self.log.info("[{0}]: Inserting the db: upload".format(task_id))
            self.db_insert_task(self.task_uuid, task_owner)

            # SEND SUBMIT MAIL
            mail_obj = Mail(task_owner=self.task_owner, mail_type='UPLOAD_START', task_id=task_id, task_uuid=self.task_uuid, dep_file_path=dep_file_path, cmd=cmd)
            mail_obj.send_()
            self.log.info("[{0}]: UPLOAD START MAIL SENT".format(task_id))

            self.log.info("[{0}]: Dep file: {1}".format(task_id, dep_file_path))
        # Retry
        else:
           #6. Retry log
           self.log.info("[{0}]: Retry # {1}, task_uuid {2}".format(task_id, count, self.task_uuid)) 
 
           #7. DB update
           #self.db_update_task(self.task_uuid, 'active', count=count)

        try:
            self.log.info("[{0}]: Start command: {1}".format(task_id, cmd))
            retval = self.exec_cmd(task_id, cmd)
            self.log.info("[{0}]: Finish command: {1}".format(task_id, cmd))

            #db_update_task
            self.log.info("[{0}]: Updating the db: upload".format(task_id))
            self.db_update_task(self.task_uuid, retval=retval, count=count)

            return "Upload Success!"
        except TaskException as e:
            #4. Retry if not user aborted
            if self.error_type is not None and self.error_type != 'user_abort':
                #8. DB update
                #self.db_update_task(self.task_uuid, 'failed', count=count, exc=e.message)
                self.db_update_task(self.task_uuid, 'retry', count=count, exc=e.message)
                self.retry(args=[task_owner, dep_file_path, cmd, task_uuid, unique_id, alf_script, operation, count+1], exc=e, kwargs=kwargs)
            elif self.error_type == 'user_abort':
                raise TaskException(e.message)

        """
        if retval == 0:
            #msg = "[{0}]: Sync successful".format(task_id)
            #self.log.info(msg)
            return task_id
        else:
            # raise an error
            msg = "[{0}]: Upload failed: {0}".format(task_id)
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
        """  

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        retry_count = args[7] + 1
        #5. Retry send_ mail
        msg = "[{0}]: Upload Failed: {1}! Retrying... attempt # {2}".format(task_id, exc.message, retry_count)
        self.log.info(msg)
        # SEND RETRY MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='UPLOAD_RETRY', exc=exc, task_id=task_id, task_uuid=self.task_uuid, einfo=einfo, retry=retry_count)  
        mail_obj.send_()
        self.log.info("[{0}]: UPLOAD RETRY MAIL SENT".format(task_id))
        

    def on_success(self, retval, task_id, args, kwargs):
        # SEND DONE MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='UPLOAD_COMPLETE', task_id=task_id, task_uuid=self.task_uuid, retval=retval, count=args[7])        
        mail_obj.send_()
        self.log.info("[{0}]: UPLOAD COMPLETE MAIL SENT".format(task_id))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = "[{0}]: Upload failed: {1}".format(task_id, exc.message)
        self.log.info(msg)

        #db_update_task
        self.db_update_task(self.task_uuid, 'failed', exc=exc.message, count=args[7])

        # SEND FAIL MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='UPLOAD_FAIL', exc=exc, task_id=task_id, task_uuid=self.task_uuid, einfo=einfo)        
        mail_obj.send_()
        self.log.info("[{0}]: UPLOAD FAIL MAIL SENT".format(task_id))

    def db_insert_task(self, task_id, task_owner, status='active'):
        db_obj = QueueDb()
        client = db_obj.client()
        # collection
        task_collection = client.queue.tasks

        self.log.info("+++++++++++++++++++++")
        self.log.info("task_id: {0}".format(task_id))
        self.log.info("+++++++++++++++++++++")
        
        task_doc = task_collection.find_one({'task_id' : task_id})
        '''
        if not task_doc:
            task_doc = {}
            task_doc['task_id'] = task_id
            task_doc['upload_id'] = self.request.id
        '''

        task_doc['upload_start'] = datetime.datetime.now()
        task_doc['upload_status'] = status
        task_doc['upload_retry_count'] = 0

        task_collection.save(task_doc)


    def db_update_task(self, task_id, status='done', **kwargs) :
        db_obj = QueueDb()
        client = db_obj.client()
        # count
        count = kwargs.get('count')

        # collection
        task_collection = client.queue.tasks

        task_doc = task_collection.find_one({'task_id' : task_id})
        '''
        if not task_doc:
            task_doc = {}
            task_doc['task_id'] = task_id
        '''
  
        if count is not None and count > 0:
            retry_count = count
            if status == 'active':
                task_doc['upload_retry_count'] = retry_count
                task_doc['upload_retry_{0}_start'.format(retry_count)] = datetime.datetime.now()
                task_doc['upload_retry_{0}_status'.format(retry_count)] = status
            elif status == 'failed' or status == 'retry':
                task_doc['upload_retry_{0}_stop'.format(retry_count)] = datetime.datetime.now()
                task_doc['upload_retry_{0}_status'.format(retry_count)] = status 
                task_doc['upload_status'] = status
                task_doc['upload_retry_{0}_exception'.format(retry_count)] = kwargs.get('exc')
                task_doc['upload_retry_{0}_einfo'.format(retry_count)] = kwargs.get('einfo')
                #if retry_count == 2 or self.error_type == 'user_abort':
                    #task_doc['upload_exception'] = kwargs.get('exc')
                    #task_doc['upload_einfo'] = kwargs.get('einfo')
            elif status == 'done':
                task_doc['upload_retry_{0}_status'.format(retry_count)] = status
                task_doc['upload_retry_{0}_stop'.format(retry_count)] = datetime.datetime.now()
                task_doc['upload_stop'] = datetime.datetime.now()
                task_doc['upload_status'] = status
                task_doc['upload_retval'] = kwargs.get('retval')
        else:
            if status == 'done':
                task_doc['upload_stop'] = datetime.datetime.now()
                task_doc['upload_status'] = status
                task_doc['upload_retval'] = kwargs.get('retval')
            #elif status == 'failed' and self.error_type == 'user_abort':
            elif status == 'failed' or status == 'retry':
                task_doc['upload_status'] = status
                task_doc['upload_exception'] = kwargs.get('exc')
                task_doc['upload_einfo'] = kwargs.get('einfo')
                
            '''
            if status == 'failed':
                task_doc['upload_exception'] = kwargs.get('exc')
                task_doc['upload_einfo'] = kwargs.get('einfo')
            else:
                task_doc['upload_retval'] = kwargs.get('retval')
            '''

        # save
        task_collection.save(task_doc)

    def send_mail(**kwargs):
        mail_obj = Mail(**kwargs)        
        mail_obj.send_()
        self.log.info("[{0}]: UPLOAD FAIL MAIL SENT".format(task_id))


@app.task
@register_task_logger(__name__)
class SpoolTestTask(Task):
    max_retries = 3
    default_retry_delay = 3

    def run(self, task_owner, engine, priority, alf_script, task_uuid, unique_id, dep_file, operation, tactic_file, task_str, count, **kwargs):
        task_id = self.request.id
        self.task_uuid = task_uuid

        self.error_type = None

        self.task_owner = task_owner
        self.unique_id = unique_id
        self.dep_file = dep_file
        self.operation = operation
        self.alf_script = alf_script
        self.tactic_file = tactic_file
        self.task_str = task_str

        # First try 
        if count == 0:
            self.log.info("[{0}]: Inserting into the db: spool".format(task_id))
            self.db_insert_task(self.task_uuid)
        # Retry
        else:
           #6. Retry log
           self.log.info("[{0}]: Retry # {1}, task_uuid {2}".format(task_id, count, self.task_uuid)) 

        try:
            cmd = "task_queue.rfm.tractor.Spool(['--user={0}', --engine={1}', '--priority={2}', '{3}'])".format(task_owner, engine, priority, alf_script, tactic_file, task_str)
            self.log.info("[{0}]: Start command: {1}".format(task_id, cmd))

            # Execute `cmd`
            import paramiko

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('119.81.131.43', port=7001, username='root', password='barajoun@2014')

            cmd = "{0} {1} {2};chown render:render {1};chmod 777 {1}".format(FIX_MAYA_FILE_BIN, self.tactic_file, self.task_str)
            print >>sys.stderr, "Executing cmd: ", cmd

            stdin, stdout, stderr = ssh.exec_command(cmd)

            stdout_msg = stdout.readlines()
            stderr_msg = stderr.readlines()

            print >>sys.stderr, 'STDOUT: ', stdout_msg
            print >>sys.stderr, 'STDERR: ', stderr_msg
            
            self.log.info("[{0}]: FIX_MAYA_FILE_BIN stdout: {1}".format(task_id, stdout_msg))
            self.log.info("[{0}]: FIX_MAYA_FILE_BIN stderr: {1}".format(task_id, stderr_msg))

            import task_queue.rfm.tractor
            import json
            retval = task_queue.rfm.tractor.Spool(['--user={0}'.format(task_owner), '--engine={0}'.format(engine), '--priority={0}'.format(priority), '{0}'.format(alf_script)])
            # Get the jid
            task_jid = json.loads(retval).get('jid')

            # Connect to the tractor engine in China, for now via the proxy in sgp
            tq.setEngineClientParam(hostname="119.81.131.43", port=1503, user=task_owner, debug=True)
            # Add the upload task ID as metadata to the task
            metadata = task_id.split('-')[1]
            tq.jattr('jid={0}'.format(task_jid), key='metadata', value=metadata)
            tq.closeEngineClient()
            self.log.info("[{0}]: Updated {1} with metadata: {2}".format(task_id, task_jid, metadata))

            self.log.info("[{0}]: Finish command: {1}".format(task_id, cmd))

            #db_update_task
            self.log.info("[{0}]: Updating the db: spool".format(task_id))
            self.db_update_task(self.task_uuid, retval=retval)

            return task_jid

            '''
            raise Exception("foo bar")
            '''
        except Exception as e:
            #8. DB update
            self.db_update_task(self.task_uuid, 'retry', count=count, exc=e.message)
            self.retry(args=[task_owner, engine, priority, alf_script, task_uuid, unique_id, dep_file, operation, tactic_file, task_str, count+1], exc=e, kwargs=kwargs)

        """
        if retval == 0:
            #msg = "[{0}]: Sync successful".format(task_id)
            #self.log.info(msg)
            return task_id
        else:
            # raise an error
            msg = "[{0}]: Spool failed: {0}".format(task_id)
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
        """  

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        retry_count = args[8] + 1
        #5. Retry send_ mail
        msg = "[{0}]: Spool Failed: {1}! Retrying... attempt # {2}".format(task_id, exc.message, retry_count)
        self.log.info(msg)
        # SEND RETRY MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='SPOOL_RETRY', exc=exc, task_id=task_id, task_uuid=self.task_uuid, einfo=einfo, retry=retry_count)  
        mail_obj.send_()
        self.log.info("[{0}]: SPOOL RETRY MAIL SENT".format(task_id))

    def on_success(self, retval, task_id, args, kwargs):
        # SEND DONE MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='SPOOL_COMPLETE', task_id=task_id, task_uuid=self.task_uuid, retval=retval, count=args[8])        
        mail_obj.send_()
        self.log.info("[{0}]: SPOOL COMPLETE MAIL SENT".format(task_id))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = "[{0}]: Spool failed: {1}".format(task_id, exc.message)
        self.log.info(msg)

        #db_update_task
        self.db_update_task(self.task_uuid, 'failed', exc=exc.message, count=args[8])

        '''
        # SEND FAIL MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='SPOOL_FAIL', exc=exc, task_id=task_id, task_uuid=self.task_uuid, einfo=einfo)        
        mail_obj.send_()
        self.log.info("[{0}]: SPOOL FAIL MAIL SENT".format(task_id))
        '''

    def db_insert_task(self, task_id, status='active'):
        db_obj = QueueDb()
        client = db_obj.client()
        # collection
        task_collection = client.queue.tasks

        self.log.info("+++++++++++++++++++++")
        self.log.info("task_id: {0}".format(task_id))
        self.log.info("+++++++++++++++++++++")
        
        task_doc = task_collection.find_one({'task_id' : task_id})
        '''
        if not task_doc:
            task_doc = {}
            task_doc['task_id'] = task_id
            task_doc['spool_id'] = self.request.id
        '''

        task_doc['spool_start'] = datetime.datetime.now()
        task_doc['spool_status'] = status
        task_doc['spool_retry_count'] = 0

        task_collection.save(task_doc)


    def db_update_task(self, task_id, status='done', **kwargs) :
        db_obj = QueueDb()
        client = db_obj.client()
        # count
        count = kwargs.get('count')

        # collection
        task_collection = client.queue.tasks

        task_doc = task_collection.find_one({'task_id' : task_id})
        '''
        if not task_doc:
            task_doc = {}
            task_doc['task_id'] = task_id
        '''
  
        if count is not None and count > 0:
            retry_count = count
            if status == 'active':
                task_doc['spool_retry_count'] = retry_count
                task_doc['spool_retry_{0}_start'.format(retry_count)] = datetime.datetime.now()
                task_doc['spool_retry_{0}_status'.format(retry_count)] = status
            elif status == 'failed' or status == 'retry':
                task_doc['spool_retry_{0}_stop'.format(retry_count)] = datetime.datetime.now()
                task_doc['spool_retry_{0}_status'.format(retry_count)] = status 
                task_doc['spool_status'] = status
                task_doc['spool_retry_{0}_exception'.format(retry_count)] = kwargs.get('exc')
                task_doc['spool_retry_{0}_einfo'.format(retry_count)] = kwargs.get('einfo')
                if retry_count == 2 or self.error_type == 'user_abort':
                    task_doc['spool_exception'] = kwargs.get('exc')
                    task_doc['spool_einfo'] = kwargs.get('einfo')
            elif status == 'done':
                task_doc['spool_retry_{0}_status'.format(retry_count)] = status
                task_doc['spool_retry_{0}_stop'.format(retry_count)] = datetime.datetime.now()
                task_doc['spool_stop'] = datetime.datetime.now()
                task_doc['spool_status'] = status
                task_doc['spool_retval'] = kwargs.get('retval')
        else:
            if status == 'done':
                task_doc['spool_stop'] = datetime.datetime.now()
                task_doc['spool_status'] = status
                task_doc['spool_retval'] = kwargs.get('retval')
            elif status == 'failed' or status == 'retry':
                task_doc['spool_exception'] = kwargs.get('exc')
                task_doc['spool_status'] = status
                task_doc['spool_einfo'] = kwargs.get('einfo')
                
            '''
            if status == 'failed':
                task_doc['spool_exception'] = kwargs.get('exc')
                task_doc['spool_einfo'] = kwargs.get('einfo')
            else:
                task_doc['spool_retval'] = kwargs.get('retval')
            '''

        # save
        task_collection.save(task_doc)

    def send_mail(**kwargs):
        mail_obj = Mail(**kwargs)        
        mail_obj.send_()
        self.log.info("[{0}]: SPOOL FAIL MAIL SENT".format(task_id))

@app.task
@register_task_logger(__name__)
class DownloadTestTask(Task):
    max_retries = 3
    default_retry_delay = 3

    def exec_cmd(self, task_id, cmd):
        thread = pexpect.spawn(cmd)

        self.log.info("[[{0}]: (thread) START]".format(task_id))

        cpl = thread.compile_pattern_list([pexpect.EOF,
						   '(.*)'])
        self.error_count = 0
        self.errors = []
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
                po_words = map(lambda x: x.lower(), progress_output.split('\s'))

                error_po_words = filter(lambda x: 'error' in x, po_words)
                if not error_po_words:
                    continue

                '''
                eagain_po_words = filter(lambda x: 'eagain' in x, po_words)
                if eagain_po_words:
                    self.log.info("[{0}]: Detected a CRITICAL 'eagain' error in the transfer stream, aborting: {1}".format(task_id, progress_output))
                    self.error_count += 1
                    self.errors.append(progress_output)
                    self.error_type='eagain'
                    break
                ''' 

                user_po_words = filter(lambda x: 'user' in x, po_words)
                if user_po_words:
                    self.log.info("[{0}]: Detected a user kill signal in the transfer stream, aborting: {1}".format(task_id, progress_output))
                    self.error_count += 1
                    self.errors.append(progress_output)
                    self.error_type='user_abort'
                    break

                if error_po_words:
                    self.log.info("[{0}]: Detected an error in the transfer stream, aborting: {1}".format(task_id, progress_output))
                    self.error_count += 1
                    self.errors.append(progress_output)
                    self.error_type='critical_error'
                    break

                '''
                for word in po_words:
                    if 'eagain' in word:
                #if re.match(r'.*error.*', progress_output, flags=re.IGNORECASE):
                    #if re.match(r'.*eagain.*', progress_output, flags=re.IGNORECASE):
                        # Session Stop  (Error: Session shutdown failed, Tried to write different output after EAGAIN)
                        self.log.info("[{0}]: Detected a CRITICAL error in the transfer stream, aborting: {1}".format(task_id, progress_output))
			self.error_count += 1
			self.errors.append(progress_output)
                        self.should_retry=True
                        break
                    elif 'user' in word:
                        self.log.info("[{0}]: Detected an error in the transfer stream: {1}".format(task_id, progress_output))
			self.error_count += 1
			self.errors.append(progress_output)
                        self.should_retry=False
                        break
                '''
	thread.close()

        if not self.error_count:
            return 0
        else:
            raise TaskException(self.errors[0])

    def run(self, task_owner, task_uuid, count, **kwargs):
        task_id = self.request.id
        self.task_uuid = task_uuid
        self.error_type = None
        self.task_owner = task_owner

        seq_str, _ = self.task_uuid.split('__')
        items = seq_str.split('_')
        seq = items[0]
        scn = items[1]
        shot = items[2]
        ver = items[5]

        # First try 
        if count == 0:
            self.log.info("[{0}]: Received task_id: {1}".format(task_id, self.task_uuid))
            self.log.info("[{0}]: Received task_uuid: {1}".format(self.task_uuid, self.task_uuid))

            #1.  DB insert
            self.db_insert_task(self.task_uuid)

            #2. SEND SUBMIT MAIL
            mail_obj = Mail(task_owner=self.task_owner, mail_type='DOWNLOAD_START', task_id=task_id, task_uuid=self.task_uuid)
            mail_obj.send_()
            self.log.info("[{0}]: DOWNLOAD START MAIL SENT".format(task_id))
        # Retry
        else:
           #6. Retry log
           self.log.info("[{0}]: Retry # {1}, task_uuid {2}".format(task_id, count, self.task_uuid)) 
 
           #7. DB update
           #self.db_update_task(self.task_uuid, 'active', count=count)

        #3. Command run
        # ascp -O 33001 -P 33001 -k 3 -p --overwrite=diff -d render@fox:/Tactic/bilal/render/$1/$2/$3/cg/$4 /nas/projects/Tactic/bilal/render/$1/$2/$3/cg/ #
        #cmd = "ascp -O 33001 -P 33001 -k 3 -p --overwrite=diff -d render@fox:/Tactic/bilal/render/{0}/{1}/{2}/cg/{3} /nas/projects/Tactic/bilal/render/{0}/{1}/{2}/cg/".format(seq, scn, shot, ver)
        cmd = "ascp -O 33001 -P 33001 -k 3 -p --overwrite=diff -d render@119.81.131.43:/Tactic/bilal/render/{0}/{1}/{2}/cg/{3} /nas/projects/Tactic/bilal/render/{0}/{1}/{2}/cg/".format(seq, scn, shot, ver)
        #self.log.info("[{0}]: Running cmd: {1}".format(task_id, cmd))

        try:
            retval = self.exec_cmd(task_id, cmd)
            #self.log.info("[{0}]: Finish command: {1}".format(task_id, cmd))
            #db_update_task
            self.db_update_task(self.task_uuid, retval=retval, count=count)
            return "Download Success!"
        except TaskException as e:
            #4. Retry if not user aborted
            if self.error_type is not None and self.error_type != 'user_abort':
                #8. DB update
                self.db_update_task(self.task_uuid, 'retry', count=count, exc=e.message)
                self.retry(args=[task_owner, task_uuid, count+1], exc=e, kwargs=kwargs)
            elif self.error_type == 'user_abort':
                raise TaskException(e.message)

        """
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
        """  

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        retry_count = args[2] + 1
        #5. Retry send_ mail
        msg = "[{0}]: Download Failed: {1}! Retrying... attempt # {2}".format(task_id, exc.message, retry_count)
        self.log.info(msg)
        # SEND RETRY MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='DOWNLOAD_RETRY', exc=exc, task_id=task_id, task_uuid=self.task_uuid, einfo=einfo, retry=retry_count)  
        mail_obj.send_()
        self.log.info("[{0}]: DOWNLOAD RETRY MAIL SENT".format(task_id))
        

    def on_success(self, retval, task_id, args, kwargs):
        # SEND DONE MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='DOWNLOAD_COMPLETE', task_id=task_id, task_uuid=self.task_uuid, retval=retval, count=args[2])        
        mail_obj.send_()
        self.log.info("[{0}]: DOWNLOAD COMPLETE MAIL SENT".format(task_id))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = "[{0}]: Download failed: {1}".format(task_id, exc.message)
        self.log.info(msg)

        #db_update_task
        self.db_update_task(self.task_uuid, 'failed', exc=exc.message, count=args[2])

        # SEND FAIL MAIL
        mail_obj = Mail(task_owner=self.task_owner, mail_type='DOWNLOAD_FAIL', exc=exc, task_id=task_id, task_uuid=self.task_uuid, einfo=einfo)        
        mail_obj.send_()
        self.log.info("[{0}]: DOWNLOAD FAIL MAIL SENT".format(task_id))

    def db_insert_task(self, task_id, status='active'):
        db_obj = QueueDb()
        client = db_obj.client()
        # collection
        task_collection = client.queue.tasks

        self.log.info("+++++++++++++++++++++")
        self.log.info("task_id: {0}".format(task_id))
        self.log.info("+++++++++++++++++++++")
        
        task_doc = task_collection.find_one({'task_id' : task_id})
        '''
        if not task_doc:
            task_doc = {}
            task_doc['task_id'] = task_id
            task_doc['download_id'] = self.request.id
        '''

        task_doc['download_start'] = datetime.datetime.now()
        task_doc['download_status'] = status
        task_doc['download_retry_count'] = 0

        task_collection.save(task_doc)


    def db_update_task(self, task_id, status='done', **kwargs) :
        db_obj = QueueDb()
        client = db_obj.client()
        # count
        count = kwargs.get('count')

        # collection
        task_collection = client.queue.tasks

        task_doc = task_collection.find_one({'task_id' : task_id})
        '''
        if not task_doc:
            task_doc = {}
            task_doc['task_id'] = task_id
        '''
  
        if count is not None and count > 0:
            retry_count = count
            if status == 'active':
                task_doc['download_retry_count'] = retry_count
                task_doc['download_retry_{0}_start'.format(retry_count)] = datetime.datetime.now()
                task_doc['download_retry_{0}_status'.format(retry_count)] = status
            elif status == 'failed' or status == 'retry':
                task_doc['download_retry_{0}_stop'.format(retry_count)] = datetime.datetime.now()
                task_doc['download_retry_{0}_status'.format(retry_count)] = status 
                task_doc['download_status'] = status
                task_doc['download_retry_{0}_exception'.format(retry_count)] = kwargs.get('exc')
                task_doc['download_retry_{0}_einfo'.format(retry_count)] = kwargs.get('einfo')
                #if retry_count == 2 or self.error_type == 'user_abort':
                #    task_doc['download_exception'] = kwargs.get('exc')
                #    task_doc['download_einfo'] = kwargs.get('einfo')
            elif status == 'done':
                task_doc['download_retry_{0}_status'.format(retry_count)] = status
                task_doc['download_retry_{0}_stop'.format(retry_count)] = datetime.datetime.now()
                task_doc['download_stop'] = datetime.datetime.now()
                task_doc['download_status'] = status
                task_doc['download_retval'] = kwargs.get('retval')
        else:
            if status == 'done':
                task_doc['download_stop'] = datetime.datetime.now()
                task_doc['download_status'] = status
                task_doc['download_retval'] = kwargs.get('retval')
            #elif status == 'failed' and self.error_type == 'user_abort':
            elif status == 'failed' or status == 'retry':
                task_doc['download_exception'] = kwargs.get('exc')
                task_doc['download_status'] = status
                task_doc['download_einfo'] = kwargs.get('einfo')
                
            '''
            if status == 'failed':
                task_doc['download_exception'] = kwargs.get('exc')
                task_doc['download_einfo'] = kwargs.get('einfo')
            else:
                task_doc['download_retval'] = kwargs.get('retval')
            '''

        # save
        task_collection.save(task_doc)

    def send_mail(**kwargs):
        mail_obj = Mail(**kwargs)        
        mail_obj.send_()
        self.log.info("[{0}]: DOWNLOAD FAIL MAIL SENT".format(task_id))

@app.task
@register_task_logger(__name__)
class TestTask(Task):
    max_retries=5
    # define celery task
    def run(self, x, y, retry_interval, count=1, **kwargs):
        """
        randomly raise exception, count attempts
        """
        i = random.randint(1, 10)
        self.log.info("Count: {0}, {1}".format(count, i))
        if i > 4:
            try:
                raise Exception('Something bad happened', count)
            except Exception, e:
                # retry task in <retry_interval> seconds
                self.retry(args=[x, y, retry_interval, e[1]+1], exc=e, countdown=retry_interval, kwargs=kwargs)
        return x*y, count

        """
        try:
	    task_id = self.request.id

	    #logger = get_or_create_task_logger(func=add)
	    self.log.info("[%s]: add(%d, %d)" % (task_id, x, y))

	    result = x + y
	    self.log.info("[%s]: add(%d, %d) result: %d" % (task_id, x, y, result))
        except Exception as exc:
            self.retry(exc=exc, countdown=10)

	return result
        """

    def on_success(self, retval, task_id, args, kwargs):
        self.log.info("[{0}]: SUCCESS : {1}".format(task_id, retval))

        """
        # SEND DONE MAIL
        mail_obj = Mail(mail_type='UPLOAD_COMPLETE', task_id=task_id, retval=retval)        
        mail_obj.send_()
        self.log.info("[{0}]: UPLOAD COMPLETE MAIL SENT".format(task_id))
        """

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.log.info("[{0}]: FAILURE : {1}".format(task_id, exc))

        """
        # SEND FAIL MAIL
        mail_obj = Mail(mail_type='UPLOAD_FAIL', exc=exc, task_id=task_id, einfo=einfo)        
        mail_obj.send_()
        self.log.info("[{0}]: UPLOAD FAIL MAIL SENT".format(task_id))
        """

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self.log.info("[{0}]: Exception: {1}, RETRY# {2}".format(task_id, exc, args[3]))

        """
        # SEND FAIL MAIL
        mail_obj = Mail(mail_type='UPLOAD_FAIL', exc=exc, task_id=task_id, einfo=einfo)        
        mail_obj.send_()
        self.log.info("[{0}]: UPLOAD FAIL MAIL SENT".format(task_id))
        """

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


@app.task
def add(x, y):
    task_id = add.request.id
    logger = get_or_create_task_logger(func=add)
    logger_func(logger, "[%s]: add(%d, %d)" % (task_id, x, y))

    q = Queue()

    t = threading.Thread(target=add_worker, name="add_worker", args=(q,)) 
    logger_func(logger, "New thread starting")
    t.start()

    while t.is_alive():
        print("From the Main-thread: ", q.get())

    t.join()
    logger_func(logger, "New thread finishing")

    result = x + y
    logger_func(logger, "Returning add(%d, %d) result: %d" % (x, y, result))
    return result

@app.task
def mult(x, y):
    logger = get_or_create_task_logger(func=mult)
    logger_func(logger, "Calling task mult(%d, %d)" % (x, y))

    p = multiprocessing.Process(target=mult_worker, name="mult_worker") 
    p.start()
    p.join()

    return x * y
"""
