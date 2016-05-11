#!/usr/bin/env python
import sys
import os
import subprocess

cmd = subprocess.Popen('prman -progress /xsan/14_Feb_Bahrain/renderman/flagRM/rib/0002/cameraShape2_Final.0002.rib', shell=True, stdout=subprocess.STDOUT)
for i in cmd.stdout.readline():
    print 'Belal Salem'
    print >>sys.stdout,  '80%'
    if str(i).strip == '80%':
        print >>sys.stdout, '80% of the job was finished'

    sys.stdout.flush()
    sys.stdout.write('Belal Salem')
    