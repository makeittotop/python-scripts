# ../log.py
import logging, sys

from celery.utils.log import get_task_logger
 
def register_task_logger(module_name):
    """Instantiate a logger at the decorated class instance level."""
    def wrapper(cls):
        #cls.log = get_task_logger('%s.%s' % (module_name, cls.__name__))
        cls.log = logging.getLogger('%s.%s' % (module_name, cls.__name__))

        if len(cls.log.handlers) == 0:
            file_handler = logging.FileHandler('/var/log/task_queue/%s.log' % cls.__name__)
            formatter = logging.Formatter(
                 '%(asctime)s %(levelname)s [%(name)s: %(lineno)s] -- %(message)s',
                 '%m-%d-%Y %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            cls.log.addHandler(file_handler)
            cls.log.setLevel(logging.DEBUG)

        return cls
    return wrapper

def get_or_create_task_logger(**kwargs):
    """ A helper function to create function specific logger lazily. """

    # https://docs.python.org/2/library/logging.html?highlight=logging#logging.getLogger
    # This will always result the same singleton logger
    # based on the task's function name (does not check cross-module name clash, 
    # for demo purposes only)
    logger = logging.getLogger(kwargs['func'].__name__)

    # Add our custom logging handler for this logger only
    # You could also peek into Celery task context variables here
    #  http://celery.readthedocs.org/en/latest/userguide/tasks.html#context
    if len(logger.handlers) == 0:
        # Log to output file based on the function name
        hdlr = logging.FileHandler('/var/log/task_queue/%s.log' % kwargs['func'].__name__)
        formatter = logging.Formatter(
             '%(asctime)s %(levelname)s [%(name)s: %(lineno)s] -- %(message)s',
             '%m-%d-%Y %H:%M:%S'
        )
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.setLevel(logging.DEBUG)

    return logger

