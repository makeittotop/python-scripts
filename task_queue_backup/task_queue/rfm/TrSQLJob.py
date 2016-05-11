#
TrFileRevisionDate = "$DateTime: 2011/04/27 14:11:52 $"

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

from TrSQLCmd  import TrSQLCmd
from TrSQLTask import TrSQLTask

import TrJob

TrJobModeObject = TrJob.TrJobModeObject
TrJobModeSummary = TrJob.TrJobModeSummary

## --------------------------------------------------------- ##
class TrSQLJob(TrJob.TrJob):

    monitorhost = "tractor-monitor"
    port        = 80
    
    def initClassVars( **settings ):
        if settings.has_key("monitor"):
            TrSQLJob.monitorhost, x, TrSQLJob.port = settings["monitor"].partition(':')
    initClassVars = staticmethod(initClassVars)
    
    def __init__(self, user, jid, **settings):
        self.sqlinfo            = None
        self.sqltimestamp       = None

        TrJob.TrJob.__init__(self, user, jid, **settings)

        if settings.has_key("monitor"):
            self.monitorhost, x, self.port = settings["monitor"].partition(':')
                    

    def createTask(self, child, jid, sjid, cmdobject, globaltasklist):
        task = TrSQLTask(child, jid, sjid, cmdobject, globaltasklist, logger=self.logger)
        return task
        

    def loadTasksAndCmds(self):
        super(TrSQLJob, self).loadTasksAndCmds()
        if self.sqlinfo and self.sqlinfo.has_key('taskinfo'): 
            self.processTaskInfo(self.sqlinfo['taskinfo'])

        if self.sqlinfo and self.sqlinfo.has_key('cmdinfo'): 
            self.processCmdInfo(self.sqlinfo['cmdinfo'])
        

    def readJobFiles(self):
        sqlfile = os.path.join(self.jobdir, "sqlinfo.log")

        self.logger.log(logging.TRACE, "trying sql file: " + sqlfile)
        # this next section is likely to fail if until a sql update has happened
        try:
            f = open(sqlfile)
            js = f.read()
            f.close()
            self.sqlinfo = eval("%s" % js)
            self.sjid = self.sqlinfo['sqljid']
            self.sqltimestamp = datetime.fromtimestamp(self.sqlinfo['timestamp'])
        except IOError:
            self.logger.log(logging.TRACE, "Error processing sqlinfo file: No file?")
        except:
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            raise

        super(TrSQLJob, self).readJobFiles()

 
    def processTaskInfo(self, taskinfo):
        for tid in self.globaltasklist:
            task = self.globaltasklist[tid]
            task.processTaskInfo(taskinfo)
    
    def processCmdInfo(self, cmdinfo):
        for tid in self.globaltasklist:
            task = self.globaltasklist[tid]
            task.processCmdInfo(cmdinfo)
    

    def saveSQLState(self, sqlObj, forceUpdate=False):
        doUpdate = False
        if self.sjid:
            doUpdate = True
            updateRequired = forceUpdate or (not self.statetime \
                or self.statetime > self.sqltimestamp)
            if updateRequired:
                sqlObj.TrSQLUpdateJob(self)
        else:
            self.sjid = sqlObj.TrSQLInsertJob(self)
            for tid in self.tasklist:
                task = self.tasklist[tid]
                task.updateSQLJid(self.sjid)
                
        if not self.sjid: return    # not use going much further

        # now process the tasks (which also processes cmds)
        for tid in self.tasklist:
            task = self.tasklist[tid]
            task.saveSQLState(sqlObj, doUpdate, self.sqltimestamp, forceUpdate)

        taskinfo = []
        for tid in self.globaltasklist:
            task = self.globaltasklist[tid]
            task.collectTaskInfo(taskinfo)
        
        cmdinfo = {}
        for tid in self.globaltasklist:
            task = self.globaltasklist[tid]
            task.collectCmdInfo(cmdinfo)
        
        sqlfile = os.path.join(self.jobdir, "sqlinfo.log")
        microtime = time.mktime(self.statetime.timetuple()) + \
            self.statetime.microsecond/1000000.0
        data = "{'sqljid': %ld, 'timestamp': %f, 'cmdinfo': %s, 'taskinfo': %s}\n" %  \
            ( self.sjid, microtime, repr(cmdinfo), repr(taskinfo) )
        try:
            f = open(sqlfile, 'w')
            f.write(data)
            f.close
        except IOError:
            # job may have been deleted, 
            self.logger.warning("Error opening sqlinfo.log file: %s.  " % sqlfile)

        except:
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            raise

    def debug(self):
        self.logger.debug("Job:jid: " + str(self.jid))
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
        self.logger.debug("SQLJob:monitorhost: " + str(self.monitorhost))
        self.logger.debug("SQLJob:port: " + str(self.port))
        
        for tid in self.tasklist:
            task = self.tasklist[tid]
            task.debug()
        
                                
