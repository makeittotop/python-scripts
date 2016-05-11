#!/usr/bin/python env

import mmap
import signal
import os, sys, time

def sig_ignore(signum, stack):
    print "Signal recieved in {0}: ".format(pid), signum
    #if pid != 0:
        #os.kill(pid, signal.SIGINT)

signal.signal(signal.SIGINT, sig_ignore)

mm = mmap.mmap(-1, 9)

pid = os.fork()

if pid == 0:
  time.sleep(80)
  print ("Child writing to anon mem:")
  mm.write("abhishek\n")
  sys.exit(0)
else:
  pid, status = os.waitpid(pid, 0)
  print "pid, status", pid, status

  print ("Parent reading from anon mem:")
  print mm.readline()

