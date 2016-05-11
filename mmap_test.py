#!/usr/bin/python env

import mmap
import os, sys

mm = mmap.mmap(-1, 9)

pid = os.fork()

if pid == 0:
  print ("Child writing to anon mem:")
  mm.write("abhishek\n")
  sys.exit(0)
else:
  pid, status = os.waitpid(pid, 0)
  print "pid, status", pid, status

  print ("Parent reading from anon mem:")
  print mm.readline()

