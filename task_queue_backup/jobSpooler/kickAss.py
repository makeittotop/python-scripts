#!/usr/bin/env python

import os
import sys

options = os.sys.argv[1:]
argLen = len(options)
if argLen > 3:
    cmd = 'cd ' + str(options[argLen -2]) + '\n'
    cmd += 'export ARNOLD_PLUGIN_PATH=$ARNOLDTREE/MtoA/shaders' + '\n'
    cmd += 'export ARNOLD_SHADERLIB_PATH=$ARNOLDTREE/MtoA/shaders' + '\n'
    cmd += 'exec kick '
    for arg in range(argLen - 2):
        cmd += options[arg] + ' '
    cmd += options[argLen -1]
    os.system(cmd)
else:
    print >>sys.stderr, 'Warning: This script should be called from inside Alfred/Tractor'
    print >>sys.stderr, '         by jobSpooler generated job scripts'
    print >>sys.stderr, ' '
    print >>sys.stderr, 'Error: No ass to kick!'
    print >>sys.stderr, ' '