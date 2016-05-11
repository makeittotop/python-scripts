#!/usr/bin/env python

import os,sys
import threading, timeit

def main():
  for i in range(1, 11):
	  for j in range(1, 11):
		  print >>sys.stderr, "{0} + {1} = {2}".format(i, j , i+j)

if __name__ == '__main__':
    print timeit.timeit(stmt="main()", setup="from __main__ import main", number=1)*1000, "ms"

