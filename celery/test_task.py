from celery import Celery, Task
import time 
 
#Specify mongodb host and datababse to connect to
BROKER_URL = 'mongodb://lic:27017/celery_test_jobs'
 
celery = Celery('EOD_TASKS',broker=BROKER_URL)
 
#Loads settings for Backend to store results of jobs 
celery.config_from_object('celeryconfig')
 
@celery.task
def add(x, y):
    time.sleep(30)
    return x + y

@celery.task
class AddTask(Task):
    def run(self, x, y):
        time.sleep(30)
        return x + y
