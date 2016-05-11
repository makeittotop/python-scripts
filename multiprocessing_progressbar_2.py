#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
from progressbar import ProgressBar, SimpleProgress
import multiprocessing as mp
from time import sleep

def my_function(letter):
    sleep(2)
    return letter+letter

dummy_args = ["A", "B", "C", "D"]
pool = mp.Pool(processes=2)

results = []

pbar = ProgressBar(widgets=[SimpleProgress()], maxval=len(dummy_args)).start()

r = [pool.apply_async(my_function, (x,), callback=results.append) for x in dummy_args]

while len(results) != len(dummy_args):
    pbar.update(len(results))
    sleep(0.5)
pbar.finish()

print results
'''

import time
from progressbar import ProgressBar
pbar = ProgressBar()

for i in pbar(range(10)):
    time.sleep(5)
    print i
