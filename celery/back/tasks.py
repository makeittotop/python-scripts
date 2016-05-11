from celery import Celery, Task
import time, pexpect, multiprocessing, threading
from Queue import Queue

from log import register_task_logger, get_or_create_task_logger

app = Celery('tasks')
app.config_from_object('celeryconfig')


def exec_cmd(cmd, logger):
    thread = pexpect.spawn(cmd)

    logger.info("[(thread) START]")

    cpl = thread.compile_pattern_list([pexpect.EOF,
                                           '(.*)'])
    while True:
        i = thread.expect_list(cpl, timeout=None)
        if i == 0: # EOF
            logger.info("[(thread) EXIT]")
            break
        elif i == 1:
            progress_output = thread.match.group(1)
            #We need to mine data for errors very carefully.
            #In case there is an error, we need to keep the task going to completion
            #But make sure that the 'CHAIN' shouldn't propogate further i.e. 'RENDER'
            #threads mustn't launch
            logger.info("[(thread) STATUS: {0}]".format(progress_output.strip()))
    thread.close()

@app.task
def sync(cmd):
    logger = get_or_create_task_logger(sync)
    logger.info("Start syncing {0}".format(cmd))

    exec_cmd(cmd, logger)

    logger.info("Finish syncing {0}".format(cmd))
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
    logger = get_or_create_task_logger(add)
    logger.info("Calling task add(%d, %d)" % (x, y))

    q = Queue()

    t = threading.Thread(target=add_worker, name="add_worker", args=(q,)) 
    logger.info("New thread starting")
    t.start()

    while t.is_alive():
        print("From the Main-thread: ", q.get())

    t.join()
    logger.info("New thread finishing")
    return x + y

@app.task
def mult(x, y):
    logger = get_or_create_task_logger(mult)
    logger.info("Calling task mult(%d, %d)" % (x, y))
    p = multiprocessing.Process(target=mult_worker, name="mult_worker") 
    p.start()
    p.join()
    return x * y

'''
@app.task
@register_task_logger(__name__)
class AddTask(Task):
    def run(self, x, y):
        self.log.info("Calling task AddTask(%d, %d)" % (x, y))
        return x + y

@app.task
@register_task_logger(__name__)
class MultTask(Task):
    def run(self, x, y):
        self.log.info("Calling task mult(%d, %d)" % (x, y))
        return x * y
'''
