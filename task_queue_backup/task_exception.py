from exceptions import Exception

class TaskException(Exception):
    def __init__(self, message, **kwargs):
        super(TaskException, self).__init__(message)
        self.errors = kwargs.get('errors')

