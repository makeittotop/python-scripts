#!/usr/bin/env python

files = [] 

try:
    for f in range(1, 1025):
        fh = open("test-{0}".format(f), "w")
        print "Opened file ...", f 
        files.append(fh)
except IOError as e:        
    print "IOError: ", str(e)

