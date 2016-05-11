#
TrFileRevisionDate = "$DateTime: 2013/02/01 15:33:43 $"

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
import logging.handlers
import errno
import re
from datetime import datetime
import time
import os.path

import TrSQLJob

## --------------------------------------------------------- ##
class TrSQL(object):
    """
    The TrSQL object is used to log tractor status to a database.
    The TrSQL object is generic, and based upon tractor initialization
    will create a datbase specific TrSQL object
    """    

    def __init__(self, **settings):
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

        self.logger.info("TrSQL object initialized")


        self.dbserver = "localhost"
        self.dbuser =  None
        self.dbtype = None
        self.db = None
        self.dbpasswd = None
        
        
        if settings.has_key("dbserver"):
            self.dbserver = settings["dbserver"]
        if settings.has_key("db"):
            self.db = settings["db"]
        if settings.has_key("dbuser"):
            self.dbuser = settings["dbuser"]
        if settings.has_key("dbtype"):
            self.dbtype = settings["dbtype"]
        if settings.has_key("dbpasswd"):
            self.dbpasswd = settings["dbpasswd"]
            
        self.initStatusVals()

        self.dispatcherlist = []
        self.monitorhost = "localhost"
        self.port = 80
        if settings.has_key("monitor"):
            self.monitorhost, x, self.port = settings["monitor"].partition(':')
        self.sessionid = "None"

    def initStatusVals(self):
        self.Unknown=0 
        self.Larval = 1
        self.Blocked = 2
        self.Thwarted = 3
        self.Ready = 4
        self.Active = 5
        self.Cleaning = 6
        self.Done = 7
        self.ErrGrpStall = 8
        self.Error = 9
        self.Linger = 10
        self.Cancelled = 11
        self.Paused = 19
        self.Enabled = 20
        self.Disabled = 21
        self.Expired = 22
        self.Idle = 30
        self.Busy = 31
        self.Shutdown = 32
        self.MtdContact = 33
        
        self.statusChars = {'U': self.Unknown,
            'B': self.Blocked,
            'T': self.Thwarted,
            'R': self.Ready,
            'A': self.Active,
            'C': self.Cleaning,
            'D': self.Done,
            'E': self.Error,
            'U': self.Unknown,
            '#': self.Unknown }
            
    def SQLExpandArray(self, arrayval):
        str = ""
        sep = ""
        if arrayval:
            for v in arrayval:
                str += v
                sep = " "
            
        return str
        
                            
    def retrievedispatcherlist(self):
        self.dispatcherlist = self.TrSQLFetchDispatcherData()


    def checkdispatcherlist(self, user, host):
        d = (user, host)
        if not d in self.dispatcherlist:
            self.TrSQLRegisterSessionData(user, host, self.port, self.sessionid, self.monitorhost)
            self.dispatcherlist.append(d)     



## -------------------Generic DB methods ---------------------- ##
## these methds are identical between the various db drivers    ##

    def TrSQLFetchResultRows(self):
        rows = self.cursor.fetchall ()
        return rows

    def TrSQLFetchResultRow(self):
        row = self.cursor.fetchone()
        return row
    
    def TrSQLQuery(self, querystring, *args):
        self.logger.log(logging.TRACE, "querystring: %s %s" % (querystring, repr(args)))
        if not self.cursor: self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(querystring, args)

        except Exception, e:
            sys.stderr.write("Error executing %s query: %s\n" % (self.dbtype, querystring))
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            return False

        self.conn.commit()
        return True
        

    def debug(self):
        self.logger.debug("Server: %s" % self.dbserver)
        self.logger.debug("User: %s" % self.dbuser)
        self.logger.debug("Passwd: %s" % self.dbpasswd)
        self.logger.debug("Type: %s" % self.dbtype)
        self.logger.debug("DB: %s" % self.db)
    

## -------------------Generic Module level methods ---------------------- ##
def trSQLInit(**settings):
    dbobject = {'MySQL': trMySQLInit,
         'Postgres': trPSQLInit}[settings["dbtype"]](**settings)
    return dbobject


def trMySQLInit(**settings):
    import TrMySQL

    dbobj = TrMySQL.TrMySQL(**settings)
    return dbobj
    
def trPSQLInit(**settings):
    import TrPSQL

    dbobj = TrPSQL.TrPSQL(**settings)
    return dbobj

def createJob(user, jid, **settings):
    job=TrSQLJob.TrSQLJob(user, jid, **settings)
    if job.valid:
        return job
    else:
        return None

def trLocateJobFile(jid, user, rootdir, logger, jobdir=None):
        if jobdir:
            if os.path.isdir(jobdir): return jobdir
                
        topdir = "%s/users/%s/jobs/J%d" % (rootdir, user, jid)
        if os.path.isdir(topdir): return topdir

        topdir = "%s/shed/users/%s/jobs/J%d" % (rootdir, user, jid)
        if os.path.isdir(topdir): return topdir

        logger.error("Job Directory: J%d not found in active or shed" % jid)
        return None


def trUpdateSQLStatusIfNeeded(jid, user, **settings):
    rootdir = "/var/spool/tractor"
    jobdir = None
    sqlobj = None
    aggressive = None
    
    if settings.has_key("rootdir"):
        rootdir = settings["rootdir"]
    if settings.has_key("jobdir"):
        jobdir = settings["jobdir"]
    if settings.has_key("sqlobj"):
        sqlobj = settings["sqlobj"]
    if settings.has_key("aggressive"):
        aggressive = settings["aggressive"]
    if settings.has_key("logger"):
        logger = settings["logger"]
    else:
        logger = logging.getLogger("tractor")
        
    jobdir = trLocateJobFile(jid, user, rootdir, logger, jobdir)
    if not jobdir: return

    doFullUpdate = True
    if aggressive:
        doFullUpdate = False
    
        sqlstat = None
        activestat = None
        
        sqlfile = os.path.join(jobdir, "sqlinfo.log")
        if not os.path.exists(sqlfile): doFullUpdate = True
        else:
            sqlstat = os.stat(sqlfile)
            
            activities = "%s/%s" % (jobdir, "activity.log")
            if os.path.exists(activities): 
                activestat = os.stat(activities)
            
            if sqlstat and activestat:
                if activestat.st_mtime > sqlstat.st_mtime:
                    doFullUpdate = True     
     
    if doFullUpdate:    
        logger.info("Synchronizing JID: %d" % jid)
        if settings.has_key("jobdir"): del settings["jobdir"]
        job = createJob(user, jid, jobdir=jobdir, mode=TrSQLJob.TrJobModeSummary, **settings)
        if not job: return
        
        if not (job.statetime and job.sqltimestamp) or (job.statetime > job.sqltimestamp):
            job.loadTasksAndCmds()
            job.taskmap = job.buildTaskMap()
            job.saveSQLState(sqlobj)
        del(job)
    
    

