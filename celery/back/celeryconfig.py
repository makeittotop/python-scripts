BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Dubai'
CELERY_ENABLE_UTC = True

CELERY_ROUTES = {
    'tasks.add': {'queue': 'lighting'},
    'tasks.mult': {'queue': 'comping'},
    'tasks.sync': {'queue': 'sync'},
}

'''
CELERY_ROUTES = {
    'tasks.AddTask': {'queue': 'lighting'},
    'tasks.MultTask': {'queue': 'comping'},
}
CELERY_ANNOTATIONS = {
    'tasks.add': {'rate_limit': '10/m'}
}
'''
