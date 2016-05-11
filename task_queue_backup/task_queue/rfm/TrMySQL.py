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
from datetime import datetime

from TrSQL import TrSQL
import MySQLdb

## --------------------------------------------------------- ##
class TrMySQL(TrSQL):
    """
    Implementation of a TrSQL object protocols for MySQL database
    """    

    def __init__(self, **settings):
        TrSQL.__init__(self, **settings)
        self.dbtype = "MySQL"
        self.conn = None
        self.cursor = None

    
    def connectToDatabase(self):
    
        self.logger.debug("TrMySQL.connectToDatabase")
        conn = None
        
        try:
            conn = MySQLdb.connect (host = self.dbserver,
                               user = self.dbuser,
                               passwd = self.dbpasswd,
                               db = self.db)
            self.curor = conn.cursor()
        
        except:
            sys.stderr.write("Error connecting to MySQL DB: ")
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            return False
            
        self.conn = conn;

        self.retrievedispatcherlist()

        return  True

    ## --------------------database methods-------------------- ##


    def TrSQLGetLastAutoID(self):
        self.TrSQLQuery("SELECT LAST_INSERT_ID()")
        row = self.TrSQLFetchResultRow()
        if row == None: return 0
        return row[0]
       
        
    def TrSQLEscapeString(self, str):
        newstr = str.replace("'", "\\'")
        newstr = newstr.replace('"', '\\"')
        return newstr;

    def SQLDateString(self, dateval):
        return dateval.strftime("%Y-%m-%d %H:%M:%S") if dateval else 0
                            

    ## -------------------- batcave methods ----------------------**

    def TrSQLFetchDispatcherData(self):

        l = []
        try:
            self.TrSQLQuery("SELECT user, host from Dispatcher")
            rows = self.TrSQLFetchResultRows()
            for row in rows:
                d = (row[0], row[1])
                l.append(d)
                
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))

        return l
    

    def TrSQLRegisterSessionData(self, user, spoolhost, port, sessionid, monitorhost):
        msg = "DELETE FROM Dispatcher WHERE user=%s AND host=%s"
        args = ( user, spoolhost )
            
        try:
            self.TrSQLQuery(msg, *args)
            
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            return
            
        msg = """INSERT INTO Dispatcher(user, host, sessionid, port, 
            maitred_host, dversion, starttime, statetime, exittime, state)
            VALUES(%.64s, %.255s, %.32s, %s, %.255s, %.255s,
            %s, %s, %s, %s)""" 

        args = ( user, spoolhost, sessionid, int(port), monitorhost, '(tractor-blade)', \
            self.SQLDateString(datetime.today()), \
            self.SQLDateString(datetime.today()), \
            self.SQLDateString(None), \
            self.Busy)
            
        try:
            self.TrSQLQuery(msg, *args)
            
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            
     
    ## --------------------   job methods   ----------------------**        
    
    def TrSQLInsertJob(self, job):

        self.checkdispatcherlist(job.user, job.host)

        id = None
        msg = """INSERT INTO Job(user, host, djid, port, title, priority, state,
            statetime, spooltime, starttime,
            donetime, slottime, deletetime,
            numTasks, active, blocked, done, error, ready,
            spoolnotes, wranglernotes, dispatchnotes, taskmap)
            VALUES(%.64s, %.255s, %s, %s,%s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s)"""

        args = (job.user, job.host, job.jid, job.port, job.title, job.priority, self.statusChars[job.state], \
            self.SQLDateString(job.statetime), \
            self.SQLDateString(job.spooltime), \
            self.SQLDateString(job.starttime), \
            self.SQLDateString(job.donetime), \
            self.SQLDateString(job.slottime), \
            self.SQLDateString(job.deletetime), \
            job.ntasks, job.active, job.blocked, job.done, job.error, job.ready,
            job.comment, '', '', job.taskmap)
        
        try:
            if (self.TrSQLQuery(msg, *args)):
                id = self.TrSQLGetLastAutoID()
            
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))

        return id
            
    def TrSQLUpdateJob(self, job):        
        self.checkdispatcherlist(job.user, job.host)
        
        msg = """UPDATE Job
            SET user=%.64s, host=%.255s, djid=%s, port=%s, 
            title=%.255s, priority=%s, state=%s,
            statetime=%s, spooltime=%s, starttime=%s,
            donetime=%s, slottime=%s, deletetime=%s,
            numTasks=%s, active=%s, blocked=%s, done=%s, error=%s, ready=%s,
            taskmap=%s
            WHERE jid = %s """ 

        args = (job.user, job.host, job.jid, job.port, \
            job.title, job.priority, self.statusChars[job.state], \
            self.SQLDateString(job.statetime), \
            self.SQLDateString(job.spooltime), \
            self.SQLDateString(job.starttime), \
            self.SQLDateString(job.donetime), \
            self.SQLDateString(job.slottime), \
            self.SQLDateString(job.deletetime), \
            job.ntasks, job.active, job.blocked, job.done, job.error, job.ready,
            job.taskmap,
            job.sjid)

        try:
            self.TrSQLQuery(msg, *args);
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
        


    ## --------------------   task methods   ----------------------**        

    def TrSQLInsertTask(self, task):
        title = self.TrSQLEscapeString(task.title)
        state = self.statusChars[task.state]
        statetime = self.SQLDateString(task.statetime)
        readytime = self.SQLDateString(task.readytime)
        msg = """INSERT INTO Task(jid, tid, title, state,
            statetime, readytime)
            VALUES(%s, %s, %.255s, %s, %s, %s)"""
        args = (task.sjid, task.tid, title, state, statetime, readytime)
        try:
            self.TrSQLQuery(msg, *args);
            return True
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            return False
            
            
    def TrSQLUpdateTask(self, task):    
        title = self.TrSQLEscapeString(task.title)
        state = self.statusChars[task.state]
        statetime = self.SQLDateString(task.statetime)
        readytime = self.SQLDateString(task.readytime)
        msg = """UPDATE Task
            SET title=%.255s, state=%s, 
            statetime=%s, readytime=%s 
            WHERE jid=%s AND tid=%s"""
        args = (title, state, statetime, readytime, task.sjid, task.tid )


        try:
            self.TrSQLQuery(msg, *args);

        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))



    ## --------------------   cmd methods   ----------------------**        

    def TrSQLInsertCmd(self, cmd):
        outid = None;    
            
        msg = """INSERT INTO Cmd (
            jid,tid, keylist, commandline,
            taglist, slots,
            starttime, endtime,
            status)
            VALUES(%s, %s, %s, %s, %s, %s,
            %s, %s , %s)"""
        args = (cmd.sjid, cmd.tid, self.SQLExpandArray(cmd.keylist), self.SQLExpandArray(cmd.commandline), \
            cmd.taglist, cmd.slots, \
            self.SQLDateString(cmd.starttime), \
            self.SQLDateString(cmd.endtime), \
            self.statusChars[cmd.status] )
    
        try:
            if self.TrSQLQuery(msg, *args):
                outid = self.TrSQLGetLastAutoID();

        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
    
        return outid;
    


    def TrSQLUpdateCmd(self, cmd):
        msg = """UPDATE Cmd
            SET slots=%s,
            starttime=%s, endtime=%s,
            status=%s
            WHERE cmdid=%s""" 
        args = (cmd.slots, \
            self.SQLDateString(cmd.starttime), \
            self.SQLDateString(cmd.endtime), \
            self.statusChars[cmd.status], cmd.scid )
    
        try:
            self.TrSQLQuery(msg, *args);

        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
    


    ## --------------------testing methods-------------------- ##

    def UpdateJobTest(self, jid):
        self.TrSQLQuery("SELECT djid FROM job WHERE jid=%ld" % jid)
        row = self.TrSQLFetchResultRow()
        djid = row[0]
        if (djid == 1):
            self.TrSQLQuery("UPDATE job SET djid=%ld WHERE jid=%ld" % (jid, jid))
        else:
            self.logger.error("djid for jid: %ld was set to %ld" % (jid, djid))
            sys.exit(25)
