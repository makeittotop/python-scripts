from __future__ import absolute_import

from queue_beta.celery import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def foo(x):
    import time
    time.sleep(60)

    return x + 56

@app.task
def factorial(x):
  try:
    import math
    return math.factorial(x)
  except Exception as e:
    return e

@app.task
def copy_file(src_files, dst='/nas/projects/development/productionTools/py_queue/test'):
    from shutil import copy2
    import sys

    for src in src_files:
            copy2(src, dst) 

