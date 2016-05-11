from __future__ import absolute_import

from celery import Celery

BROKER_URL = 'redis://16.16.16.2:4444/0'
CELERY_RESULT_BACKEND = 'redis://16.16.16.2:4444/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Dubai'
CELERY_ENABLE_UTC = True

CELERY_RESULT_PERSISTENT = True
CELERYD_PREFETCH_MULTIPLIER = 1 
CELERY_TASK_PUBLISH_RETRY = True
CELERY_TASK_PUBLISH_RETRY_POLICY = { 
     "max_retries": 2,
     "interval_start": 1,
     "interval_step": 0.5,
     "interval_max": 0.5,
}

BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}

CELERY_ROUTES = {
    'queue_beta.tasks.add': {'queue': 'hipri'},
    'queue_beta.tasks.copy_file': {'queue': 'hipri'},
    #'task_queue.tasks.UploadTask': {'queue': 'upload'},
    #'task_queue.tasks.DownloadTask': {'queue': 'download'},
}


app = Celery('queue_beta',
             #broker='amqp://',
             broker=BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['queue_beta.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()

