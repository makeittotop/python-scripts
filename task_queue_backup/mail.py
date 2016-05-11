import sys
import smtplib

class Mail(object):
    def __init__(self, **kwargs):
        self.user = 'abhishek'
        self.passwd = 'qwerty'
        self.mail_host = '172.16.10.40'
        self.port = 25
        self.to = 'a.pareek@barajoun.com'
        self.from_ = 'a.pareek@barajoun.com'
        self.server = smtplib.SMTP(self.mail_host, self.port)
        # UPLOAD
        if kwargs.get('mail_type') == 'UPLOAD_FAIL':
            self.mail_type = 'UPLOAD_FAIL'
            self.exc = kwargs.get('exc')
            self.task_id = kwargs.get('task_id')
            self.einfo = kwargs.get('einfo') 
        elif kwargs.get('mail_type') == 'UPLOAD_COMPLETE':
            self.mail_type = 'UPLOAD_COMPLETE'
            self.task_id = kwargs.get('task_id')
            self.retval = kwargs.get('retval')
        elif kwargs.get('mail_type') == 'UPLOAD_SUBMIT':
            self.mail_type = 'UPLOAD_SUBMIT'
            self.task_id = kwargs.get('task_id')
        # SPOOL
        elif kwargs.get('mail_type') == 'SPOOL_COMPLETE':
            self.mail_type = 'SPOOL_COMPLETE'
            self.task_id = kwargs.get('task_id') 
            self.retval = kwargs.get('retval')
        if kwargs.get('mail_type') == 'SPOOL_FAIL':
            self.mail_type = 'SPOOL_FAIL'
            self.exc = kwargs.get('exc')
            self.task_id = kwargs.get('task_id')
            self.einfo = kwargs.get('einfo')
        # DOWNLOAD
        if kwargs.get('mail_type') == 'DOWNLOAD_FAIL':
            self.mail_type = 'DOWNLOAD_FAIL'
            self.exc = kwargs.get('exc')
            self.task_id = kwargs.get('task_id')
            self.einfo = kwargs.get('einfo')
        elif kwargs.get('mail_type') == 'DOWNLOAD_COMPLETE':
            self.mail_type = 'DOWNLOAD_COMPLETE'
            self.task_id = kwargs.get('task_id')
            self.retval = kwargs.get('retval')
        elif kwargs.get('mail_type') == 'DOWNLOAD_SUBMIT':
            self.mail_type = 'DOWNLOAD_SUBMIT'
            self.task_id = kwargs.get('task_id')


    def send(self): 
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.user, self.passwd)

        msg = self.header() + self.body()
        #print msg

        self.server.sendmail(self.from_, self.to, msg)
        
        self.server.close()
        #print >>sys.stderr, "Done!"
                
    def header(self):
        return 'To:' + self.to + '\n' + 'From: ' + self.from_ + '\n' #+ '\n' + 'Subject: {0} notification\n'.format(type)
        
    def body(self):
        # UPLOAD
        if self.mail_type == 'UPLOAD_SUBMIT':
            body = 'Subject: Task: {0} UPLOAD SUBMISSION Mail\n'.format(self.task_id) 
            body += '\nDear reader,\n\nTask: {0} has been successfully submitted to the local queue.\n'.format(self.task_id)
        elif self.mail_type == 'UPLOAD_COMPLETE':
            body = 'Subject: Task: {0} UPLOAD COMPLETION Mail\n'.format(self.task_id) 
            body += '\nDear reader,\n\nTask: {0} has synced assets to the remote tractor queue successfully.\n\nHere is the return value from the task: {1}\n'.format(self.task_id, self.retval) 
        elif self.mail_type == 'UPLOAD_FAIL':
            body = 'Subject: Task: {0} UPLOAD FAIL Mail\n'.format(self.task_id) 
            body += '\nDear reader,\n\nTask: {0} has failed to sync assets to the remote tractor render queue.\n\nHere are the log details:\nException: {1}\nBacktrace: {2}\n'.format(self.task_id, self.exc, self.einfo)
        # SPOOL
        elif self.mail_type == 'SPOOL_COMPLETE':
            body = 'Subject: Task: {0} SPOOL COMPLETION Mail\n'.format(self.task_id)
            body += '\nDear reader,\n\nTask: {0} has been successfully spooled in the remote tractor render queue.\n\nHere is the jid from the task: {1}\n'.format(self.task_id, self.retval)        
        elif self.mail_type == 'SPOOL_FAIL':
            body = 'Subject: Task: {0} SPOOL FAIL Mail\n'.format(self.task_id)
            body += '\nDear reader,\n\nTask: {0} has failed to submit to the remote tractor render queue.\n\nHere are the log details:\nException: {1}\nBacktrace: {2}\n'.format(self.task_id, self.exc, self.einfo)
        # DOWNLOAD
        if self.mail_type == 'DOWNLOAD_SUBMIT':
            body = 'Subject: Task: {0} DOWNLOAD SUBMISSION Mail\n'.format(self.task_id)
            body += '\nDear reader,\n\nTask: {0} has been successfully submitted to the local queue.\n'.format(self.task_id)
        elif self.mail_type == 'DOWNLOAD_COMPLETE':
            body = 'Subject: Task: {0} DOWNLOAD COMPLETION Mail\n'.format(self.task_id)
            body += '\nDear reader,\n\nTask: {0} has synced assets to the remote tractor queue successfully.\n\nHere is the return value from the task: {1}\n'.format(self.task_id, self.retval)
        elif self.mail_type == 'DOWNLOAD_FAIL':
            body = 'Subject: Task: {0} DOWNLOAD FAIL Mail\n'.format(self.task_id)
            body += '\nDear reader,\n\nTask: {0} has failed to sync assets to the remote tractor render queue.\n\nHere are the log details:\nException: {1}\nBacktrace: {2}\n'.format(self.task_id, self.exc, self.einfo)

        body += '\nIn case of an emergency, please contact Pipeline/I.T.\n'
        body += '\nFrom,\nThe Queue'

        return body

