#!/usr/bin/env python

import os
import sys

options = os.sys.argv[1:]
argLen = len(options)
if argLen > 2:
    cmd = 'exec katana '
    for arg in range(argLen - 1):
        cmd += options[arg] + ' '
    cmd += options[argLen -1]
    os.system(cmd)
else:
    print >>sys.stderr, 'Warning: This script should be called from inside Alfred/Tractor'
    print >>sys.stderr, '         by jobSpooler generated job scripts'
    print >>sys.stderr, ' '
    print >>sys.stderr, 'Error: Nothing to Render!'
    print >>sys.stderr, ' '
