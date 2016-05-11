#! /usr/bin/python

import pexpect

#cmd = "waited.sh"
cmd = "python /home/abhishek/Downloads/sarge/lister.py -d 0.1 -c 100"
thread = pexpect.spawn(cmd)
print "started %s" % cmd
cpl = thread.compile_pattern_list([pexpect.EOF,
                                   'line (\d+)'])
while True:
    i = thread.expect_list(cpl, timeout=None)
    if i == 0: # EOF
        print "the sub process exited"
        break
    elif i == 1:
        waited_time = thread.match.group(1)
        print "the sub process printed line : %d " % int(waited_time)
thread.close()
