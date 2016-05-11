# ../log.py
import logging

from celery.utils.log import get_task_logger
 
def register_task_logger(module_name):
    """Instantiate a logger at the decorated class instance level."""
    def wrapper(cls):
        cls.log = get_task_logger('%s.%s' % (module_name, cls.__name__))

        if not cls.log.handlers:
            file_handler = logging.FileHandler('%s.log' % cls.__name__)
            formatter = logging.Formatter(
                 '%(asctime)s %(levelname)s [%(name)s: %(lineno)s] -- %(message)s',
                 '%m-%d-%Y %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            cls.log.addHandler(file_handler)
            cls.log.setLevel(logging.debug)

        return cls
    return wrapper

def get_or_create_task_logger(func):
    """ A helper function to create function specific logger lazily. """

    # https://docs.python.org/2/library/logging.html?highlight=logging#logging.getLogger
    # This will always result the same singleton logger
    # based on the task's function name (does not check cross-module name clash, 
    # for demo purposes only)
    logger = logging.getLogger(func.__name__)

    # Add our custom logging handler for this logger only
    # You could also peek into Celery task context variables here
    #  http://celery.readthedocs.org/en/latest/userguide/tasks.html#context
    if len(logger.handlers) == 0:
        # Log to output file based on the function name
        hdlr = logging.FileHandler('%s.log' % func.__name__)
        formatter = logging.Formatter(
             '%(asctime)s %(levelname)s [%(name)s: %(lineno)s] -- %(message)s',
             '%m-%d-%Y %H:%M:%S'
        )
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.setLevel(logging.DEBUG)

    return logger

