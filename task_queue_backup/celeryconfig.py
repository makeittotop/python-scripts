BROKER_URL = 'redis://lic:4444/0'
#CELERY_RESULT_BACKEND = 'amqp://lic:5672'
CELERY_RESULT_BACKEND = 'redis://lic:4444/0'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Dubai'
CELERY_ENABLE_UTC = True

CELERY_RESULT_PERSISTENT = True

# Enable late ack 
CELERY_ACKS_LATE = True

# RETRY
CELERY_TASK_PUBLISH_RETRY = True
CELERY_TASK_PUBLISH_RETRY_POLICY = {
     "max_retries": 2,
     "interval_start": 1,
     "interval_step": 0.5,
     "interval_max": 0.5,
}

CELERY_ROUTES = {
    #'task_queue.tasks.UploadTask': {'queue': 'upload'},
    'task_queue.tasks.SyncTask': {'queue': 'sync'},
    'task_queue.tasks.DownloadTask': {'queue': 'download'},
    'task_queue.tasks.SpoolTask': {'queue': 'spool'},
    'task_queue.tasks.TestTask': {'queue': 'test'},
}

'''
CELERY_ROUTES = {
    'task_queue.tasks.add': {'queue': 'lighting'},
    'task_queue.tasks.mult': {'queue': 'comping'},
    'task_queue.tasks.sync': {'queue': 'sync'},
}

CELERY_ANNOTATIONS = {
    'task_queue.tasks.add': {'rate_limit': '10/m'}
}

# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = True

# Name and email addresses of recipients
ADMINS = (
    ("Abhishek Pareek", "a.pareek@barajoun.com"),
    #("Cosmo Kramer", "kosmo@vandelay.com"),
)

# Email address used as sender (From field).
SERVER_EMAIL = "no-reply@vandelay.com"

# Mailserver configuration
EMAIL_HOST = "172.16.10.40"
EMAIL_PORT = 25
EMAIL_HOST_USER = "abhishek"
EMAIL_HOST_PASSWORD = "qwerty"
EMAIL_USE_TLS = True
SERVER_EMAIL = "queue-mon@lic"
'''
