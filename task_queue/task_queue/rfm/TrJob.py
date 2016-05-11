#
TrFileRevisionDate = "$DateTime: 2013/06/25 11:27:35 $"

# ____________________________________________________________________ 
# Copyright (C) 2007-2010 Pixar Animation Studios. All rights reserved.
#
# The information in this file is provided for the exclusive use of the
# software licensees of Pixar.  It is UNPUBLISHED PROPRIETARY SOURCE CODE
# of Pixar Animation Studios; the contents of this file may not be disclosed
# to third parties, copied or duplicated in any form, in whole or in part,
# without the prior written permission of Pixar Animation Studios.
# Use of copyright notice is precautionary and does not imply publication.
#
# PIXAR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT
# SHALL PIXAR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
# ____________________________________________________________________ 
#


import sys
import logging
import re
from datetime import datetime
import time
import os.path

from TrTask import TrTask

logging.TRACE=5
logging.addLevelName(logging.TRACE, 'TRACE')

TrJobModeObject = 1
TrJobModeSummary = 2

## --------------------------------------------------------- ##
class TrJob(object):

    def __init__(self, user=None, jid=None, **settings):
        
        self.mode       = TrJobModeObject
        self.valid      = False
        self.rootdir    = "/var/spool/tractor"

        # if logger hasn't been setup, then set a default logger which
        # logs only warnings or above
        if settings.has_key("logger"):
            self.logger = settings["logger"]
        else:
            self.logger = logging.getLogger("tractor")
            self.logger.setLevel(logging.WARNING)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            ch = logging.StreamHandler()
            
            ch.setLevel(logging.WARNING)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        self.logger.log(logging.TRACE, "initializing TrJob Object")
        
        self.tasklist   =   {}
        self.globaltasklist = {}
        
        self.user       =   user
        self.host       =   None
        self.jid        =   jid 
        self.sjid       =   None   # will be SQL jid
        self.title      =   None
        self.priority   =   0.0
        self.state      =   'U'
        self.statetime  =   None
        self.spooltime  =   None
        self.starttime  =   None
        self.donetime   =   None
        self.slottime   =   None
        self.deletetime =   None
        self.ntasks     =   0
        self.active     =   0
        self.blocked    =   0
        self.done       =   0
        self.ready      =   0
        self.error      =   0
        self.taskmap    =   None
        self.comment =   ""
        
        self.jobdir     =   None
        self.tasktree   =   None
        self.jobdata    =   None
        self.cmdobject  =   None
        self.activityArray = None
                
        if settings.has_key("rootdir"):
            self.rootdir = settings["rootdir"]
        if settings.has_key("mode"):
            self.mode = settings["mode"]

        if not (self.jid and self.user): return

        retry = False
        if settings.has_key("jobdir"):
            jobdir = settings["jobdir"]
        else:
            retry = True
            jobdir=jobdirPath(self.user, self.jid, self.rootdir)
        
        self.valid = self.initFromFile(jobdir)
        if (not self.valid) and retry:
            self.valid = self.initFromFile(None)
            if not self.valid: return
        
        if self.activityArray:
            self.processActivities(self.activityArray)
            
        self.taskmap = self.buildTaskMap()
        self.ntasks = len(self.globaltasklist)               
        

    def createTask(self, child, jid, sjid, cmdobject, globaltasklist):
        task = TrTask(child, jid, sjid, cmdobject, globaltasklist, logger=self.logger)
        return task
        
        
    def locateJobDir(self, jobdir):
        self.logger.log(logging.TRACE, "locateJobDir: jobdir=%s" % jobdir)
        if jobdir:
            if os.path.isdir(jobdir):
                return jobdir
            else:
                self.logger.error("Supplied jobdir: %s not found" % jobdir)
                return None
                 
        rootSlashCount = self.rootdir.count(os.sep)
        gen = os.walk(os.path.join(self.rootdir, "jobs"))
        for root,dirs,files in gen:
            slashCount = root.count(os.sep)
            levels = slashCount - rootSlashCount
            if levels == 4:     # we're in a users job directory
                l = root.split(os.sep)
                user = l[-1]
                if user != self.user:
                    del dirs[:]
                    continue
                else:
                    jidstr = "%010d" % self.jid
                    if not jidstr in dirs: 
                        del dirs[:]
                        continue
                    else:
                        return os.path.join(root, jidstr)

                    
        self.logger.error("Job Directory: J%d not found" % self.jid)
        return None
        

    def initFromFile(self, jobdir):
        self.logger.log(logging.TRACE, "InitFromFile: jobdir=%s" % jobdir)
        self.jobdir = self.locateJobDir(jobdir)
        if self.jobdir:
            self.readJobFiles()
            return True
        else:
            return False
                 
        
    def loadTasksAndCmds(self):
        taskfile = "%s/%s" % (self.jobdir, "tasktree.json")
        cmdfile = "%s/%s" % (self.jobdir, "cmdlist.json")
        
        try:
            if os.path.exists(taskfile):
                f = open(taskfile)
                js = f.read()
                f.close()
                try:
                    self.tasktree = eval(js)
                except:
                    self.valid = False
                    self.logger.error("Error evaluating json data in %s" % taskfile)
                    return    

            if os.path.exists(cmdfile):
                f = open(cmdfile)
                js = f.read()
                f.close()
                try:
                    self.cmdobject = eval(js)
                except:
                    self.valid = False
                    self.logger.error("Error evaluating json data in %s" % cmdfile)
                    return    

            if self.tasktree != None:
                for child in self.tasktree['children']:
                    task = self.createTask(child, self.jid, self.sjid, self.cmdobject, self.globaltasklist)
                    tid = child['data']['tid']
                    self.tasklist[tid]=task
            
            # re-process activities so that Tasks and Cmds are properly updated.
            if self.activityArray:
                self.processActivities(self.activityArray)

        except IOError, e:
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            raise
        except:
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            raise
    
    def readJobFiles(self):
        jobtree = "%s/%s" % (self.jobdir, "jobtree.json")
        jobinfo = "%s/%s" % (self.jobdir, "jobinfo.json")
        activityfile = "%s/%s" % (self.jobdir, "activity.log")

        try:
            if os.path.exists(jobinfo):
                f = open(jobinfo)
                js = f.read()
                f.close()
                self.jobdata = eval(js)            
            elif os.path.exists(jobtree):
                f = open(jobtree)
                js = f.read()
                f.close()
                self.jobtree = eval(js)
                self.jobdata = self.jobtree['data']
            else:
                self.logger.error("No job files found in %s" % self.jobdir)
                return

            try:
                self.host = self.jobdata['spoolhost']
                self.priority = self.jobdata['priority']
                self.title = self.jobdata['title']
                self.user = self.jobdata['user']
            except KeyError:
                if not self.jobdata.has_key('host'):
                    self.host = ""
                if not self.jobdata.has_key('title'):
                    self.title = ""
                if not self.jobdata.has_key('user'):
                    self.user = ""
            except:
                errclass, excobj = sys.exc_info()[:2]
                sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
                self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
                raise

            if self.jobdata.has_key('comment'):
                self.comment = self.jobdata['comment'];
            
            m = re.match('<@JobTimes\((\d+)\)@>', self.jobdata['jtimes'])
            spooltime = m.group(1)
            self.spooltime =  datetime.fromtimestamp(int(spooltime))       
            self.statetime = self.spooltime    

            if self.mode == TrJobModeObject:
                self.loadTasksAndCmds()

            # this next section is likely to fail if until the job is processed 
            try:
                f = open(activityfile)
                js = f.read()
                f.close()
                self.activityArray = eval("[%s]" % js)

            except IOError:
                self.logger.log(logging.TRACE, "There has been no job activity on J:" + str(self.jid))
            except:
                errclass, excobj = sys.exc_info()[:2]
                sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
                self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
                raise
                
        except IOError, e:
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            raise
        except:
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            raise

    def processActivities(self, activities):
        if not activities: return
        for activity in activities:
            timestamp, exitcode, jid, tid, cid, state, has_logs, host, blade_port, totaltasks, nactive, ndone, nerror = activity[0:13]

            statetime = datetime.fromtimestamp(timestamp)
            if not self.statetime: self.statetime = statetime
            elif statetime > self.statetime: self.statetime = statetime

            # for now assume job.state = state in activity file
            # if state == #, then this is a message, don't update state or task counts
            if state == '#':
                if tid == 0:     # this is a job status update
                    if host == 'deleted':
                        self.deletetime = self.statetime                    
            else:
                self.state = state
                self.ntasks, self.active, self.done, self.error = totaltasks, nactive, ndone, nerror
                # if some activity is happening, then job may have restarted
                # always clear donetime first
                self.donetime = None            
                
                # the log has no job start activity, so use the first cmd starttime
                if cid == 0 and not self.starttime:     
                    if state == 'A':
                        self.starttime = self.statetime
                        self.slottime = self.statetime
                    
                if tid == 0:     # this is a job status update
                    if state == 'D': self.donetime = self.statetime
                    if state == 'E': self.donetime = self.statetime

                elif self.globaltasklist.has_key(tid):
                    task = self.globaltasklist[tid]
                    task.updateStatus(cid, timestamp, state, host)


    def buildTaskMap(self):
        taskstring = ""
        for tid in self.tasklist:
            task = self.tasklist[tid]
            taskstring = task.buildTaskMap(taskstring)
        
        return taskstring
        
                    
    def setDeleted(self, deletetime=None):
        if not deletetime: deletetime = datetime.now()
        self.statetime = deletetime
        self.deletetime = self.statetime
        
    def debug(self):
        self.logger.debug("Job:jid: " + str(self.jid))
        self.logger.debug("Job:jobdir: " + str(self.jobdir))
        self.logger.debug("Job:sjid: " + str(self.sjid))
        self.logger.debug("Job:user: " + str(self.user))
        self.logger.debug("Job:host: " + str(self.host))
        self.logger.debug("Job:title: " + str(self.title))
        self.logger.debug("Job:priority: " + str(self.priority))
        self.logger.debug("Job:state: " + str(self.state))
        self.logger.debug("Job:spooltime: " + str(self.spooltime))
        self.logger.debug("Job:statetime: " + str(self.statetime))
        self.logger.debug("Job:starttime: " + str(self.starttime))
        self.logger.debug("Job:donetime: " + str(self.donetime))
        self.logger.debug("Job:deletetime: " + str(self.deletetime))
        self.logger.debug("Job:mode: " + str(self.mode))
        
        for tid in self.tasklist:
            task = self.tasklist[tid]
            task.debug()
        
## -------------------Support Functions -------------------------------------- ##

def createJob(user, jid, **settings):
    job=TrJob(user, jid, **settings)
    if job.valid:
        return job
    else:
        return None
        
def jobdirPath(user, jid, rootdir):
    jidstr = "%010d" % jid
    yearstr = jidstr[0:2]
    monthstr = jidstr[2:4]
    daystr = jidstr[4:6]
    jid = jidstr[6:]
    fullyearstr = "20" + yearstr
    topdir = "%s-%s" % (fullyearstr, monthstr)
    jiddir = "%s%s%s%s" % (yearstr, monthstr, daystr, jid)

    jobdir=os.path.join(rootdir, "jobs", topdir, daystr, user, jiddir)
    return jobdir
