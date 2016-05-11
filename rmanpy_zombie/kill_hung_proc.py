#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import psutil

# if a 'maya' process has 'init' as parent on a blade, it MUST be a zombie
maya_procs = [proc for proc in psutil.process_iter() if proc.name() == 'maya']
killable_maya_procs = filter(lambda proc: proc.parent().pid == 1, maya_procs)

for proc in killable_maya_procs:                                
    try:                                                        
        children = proc.children()                              
        for child in children:                                  
            try:                                                
                print >>sys.stderr, "Terminating child process: ({0}:{1}) of parent: ({2}:{3}) ...".format(child.pid, child.name(), proc.pid, proc.name())
                child.kill()                                                                                                                              
            except:                                                                                                                                       
                e = sys.exc_info()[0]                                                                                                                     
                print >>sys.stderr, "Exception: {0} for child process: ({1}:{2})".format(e, child.pid, child.name())                                      
        print >>sys.stderr, "Terminating process: ({0}:{1}) ...".format(proc.pid, proc.name())                                                            
        proc.kill()
    except:        
        e = sys.exc_info()[0]
        print >>sys.stderr, "Exception: {0} for process: ({1}:{2})".format(e, proc.pid, proc.name())

maya_bin_procs = [proc for proc in psutil.process_iter() if proc.name() == 'maya.bin']
killable_maya_bin_procs = filter(lambda proc: proc.parent().pid == 1, maya_bin_procs)

for proc in killable_maya_bin_procs:                                
    try:                                                        
        children = proc.children()                              
        for child in children:                                  
            try:                                                
                print >>sys.stderr, "Terminating child process: ({0}:{1}) of parent: ({2}:{3}) ...".format(child.pid, child.name(), proc.pid, proc.name())
                child.kill()                                                                                                                              
            except:                                                                                                                                       
                e = sys.exc_info()[0]                                                                                                                     
                print >>sys.stderr, "Exception: {0} for child process: ({1}:{2})".format(e, child.pid, child.name())                                      
        print >>sys.stderr, "Terminating process: ({0}:{1}) ...".format(proc.pid, proc.name())                                                            
        proc.kill()
    except:        
        e = sys.exc_info()[0]
        print >>sys.stderr, "Exception: {0} for process: ({1}:{2})".format(e, proc.pid, proc.name())