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
import logging.handlers
import errno
from datetime import datetime

from TrSQL import TrSQL
import pgdb

## --------------------------------------------------------- ##
class TrPSQL(TrSQL):
    """
    Implementation of a TrSQL object protocols for Postgres database
    """    

    def __init__(self, **settings):
        TrSQL.__init__(self, **settings)
        self.dbtype = "Postgres"
        self.conn = None
        self.cursor = None
        self.logger.info("TrPSQL object initialized")
        
    
    def connectToDatabase(self):
    
        self.logger.info("TrPSQL.connectToDatabase")
        conn = None
        
        try:
            conn = pgdb.connect (host = self.dbserver,
                               user = self.dbuser,
                               password = self.dbpasswd,
                               database = self.db)
        
        except Exception, e:
            sys.stderr.write("Error connecting to Postgres DB: ")
            errclass, excobj = sys.exc_info()[:2]
            sys.stderr.write("%s - %s\n" % (errclass.__name__, str(excobj)))
            
            return False
            
        self.logger.info("conn: " + repr(conn))
        self.conn = conn;

        self.retrievedispatcherlist()

        return  True


    ## -------------------- database methods ----------------------**        

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
        return dateval.strftime("'%Y-%m-%d %H:%M:%S'") if dateval else 'NULL'
        

    ## --------------------batcave methods-------------------- ##
    
    def TrSQLFetchDispatcherData(self):

        l = []
        try:
            self.TrSQLQuery("SELECT duser, host from dispatcher")
            rows = self.TrSQLFetchResultRows()
            for row in rows:
                d = (row[0], row[1])
                l.append(d)
                
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))

        return l
    

    def TrSQLRegisterSessionData(self, user, spoolhost, port, sessionid, monitorhost):
        msg = """DELETE FROM dispatcher WHERE duser='%s' AND host='%s'""" % \
            ( user, spoolhost )
            
        try:
            self.TrSQLQuery(msg)
            
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            return
            
        msg = """INSERT INTO dispatcher(duser, host, sessionid, port, 
            maitred_host, dversion, starttime, statetime, exittime, state)
            VALUES('%.64s', '%.255s', '%.32s', %d, '%.255s', '%.255s',
            %s, %s, %s, %d)""" % \
            ( user, spoolhost, sessionid, int(port), monitorhost, '(tractor-blade)', \
            self.SQLDateString(datetime.today()), \
            self.SQLDateString(datetime.today()), \
            self.SQLDateString(None), \
            self.Busy)
            
        try:
            self.TrSQLQuery(msg)
            
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
            
     

    ## --------------------   job methods   ----------------------**        


    def TrSQLInsertJob(self, job):

        self.checkdispatcherlist(job.user, job.host)

        id = None
        msg = """INSERT INTO job(juser, host, djid, port, title, priority, state,
            statetime, spooltime, starttime,
            donetime, slottime, deletetime,
            numTasks, active, blocked, done, error, ready,
            spoolnotes, wranglernotes, dispatchnotes, taskmap)
            VALUES('%.64s', '%.255s', %d, '%s','%.255s', %d, %d,
            %s, %s, %s, %s, %s, %s,
            %d, %d, %d, %d, %d, %d,
            '%s', '%s', '%s', '%s')"""  %  \
            (job.user, job.host, job.jid, job.port, job.title, job.priority, self.statusChars[job.state], \
            self.SQLDateString(job.statetime), \
            self.SQLDateString(job.spooltime), \
            self.SQLDateString(job.starttime), \
            self.SQLDateString(job.donetime), \
            self.SQLDateString(job.slottime), \
            self.SQLDateString(job.deletetime), \
            job.ntasks, job.active, job.blocked, job.done, job.error, job.ready,
            job.comment, '', '', job.taskmap)
        
        try:
            if (self.TrSQLQuery(msg)):
                self.TrSQLQuery("SELECT currval('job_jid_seq')")
                row = self.TrSQLFetchResultRow()
                if row != None:
                    id = row[0]
            
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))

        return id
            
    def TrSQLUpdateJob(self, job):
        self.checkdispatcherlist(job.user, job.host)

        msg = """UPDATE job
            SET juser='%.64s', host='%.255s', djid=%d, port='%s', 
            title='%.255s', priority=%d, state=%d,
            statetime=%s, spooltime=%s, starttime=%s,
            donetime=%s, slottime=%s, deletetime=%s,
            numTasks=%d, active=%d, blocked=%d, done=%d, error=%d, ready=%d,
            taskmap='%s'
            WHERE jid = %d """ %  \
            (job.user, job.host, job.jid, job.port, \
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
            self.TrSQLQuery(msg);
        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
        


    ## --------------------   task methods   ----------------------**        

    def TrSQLInsertTask(self, task):
        title = self.TrSQLEscapeString(task.title)
        state = self.statusChars[task.state]
        statetime = self.SQLDateString(task.statetime)
        readytime = self.SQLDateString(task.readytime)
        msg = """INSERT INTO task(jid, tid, title, state,
            statetime, readytime)
            VALUES(%.0lf, %d, '%.255s', %d, %s, %s)""" % \
            (task.sjid, task.tid, title, state, statetime, readytime)
        try:
            self.TrSQLQuery(msg);
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
        msg = """UPDATE task
            SET title='%.255s', state=%d, 
            statetime=%s, readytime=%s 
            WHERE jid=%ld AND tid=%d""" % \
            (title, state, statetime, readytime, task.sjid, task.tid, )


        try:
            self.TrSQLQuery(msg);

        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))



    ## --------------------   cmd methods   ----------------------**        

    def TrSQLInsertCmd(self, cmd):
        outid = None;    
            
        msg = """INSERT INTO cmd (
            jid,tid, keylist, commandline,
            taglist, slots,
            starttime, endtime,
            status)
            VALUES(%ld, %d, '%s', '%s', '%s', '%s',
            %s, %s , %d)""" % \
            (cmd.sjid, cmd.tid, self.SQLExpandArray(cmd.keylist), self.SQLExpandArray(cmd.commandline), \
            cmd.taglist, cmd.slots, \
            self.SQLDateString(cmd.starttime), \
            self.SQLDateString(cmd.endtime), \
            self.statusChars[cmd.status] )
    
        try:
            if self.TrSQLQuery(msg):
                self.TrSQLQuery("SELECT currval('cmd_cmdid_seq')")
                row = self.TrSQLFetchResultRow()
                if row != None:
                    outid = row[0]

        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
    
        return outid;
    


    def TrSQLUpdateCmd(self, cmd):
        msg = """UPDATE Cmd
            SET slots='%s',
            starttime=%s, endtime=%s,
            status=%d
            WHERE cmdid=%ld""" % \
            (cmd.slots, \
            self.SQLDateString(cmd.starttime), \
            self.SQLDateString(cmd.endtime), \
            self.statusChars[cmd.status], cmd.scid )
    
        try:
            self.TrSQLQuery(msg);

        except:
            errclass, excobj = sys.exc_info()[:2]
            self.logger.error("%s - %s\n" % (errclass.__name__, str(excobj)))
    



    ## --------------------testing methods-------------------- ##


    def UpdateJobTest(self, jid):
        self.TrSQLQuery("SELECT djid FROM job WHERE jid=%ld" % jid)
        djid = self.TrSQLFetchResultRow()[0]
        if (djid == 1):
            self.TrSQLQuery("UPDATE job SET djid=%ld WHERE jid=%ld" % (jid, jid))
        else:
            self.logger.error("djid for jid: %ld was set to %ld" % (jid, djid))
            sys.exit(25)
            
