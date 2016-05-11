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

import logging
from datetime import datetime

from TrTask    import TrTask
from TrSQLCmd  import TrSQLCmd

## --------------------------------------------------------- ##
class TrSQLTask(TrTask):

    def __init__(self, tobject, jid, sjid, cmdobject, globaltasklist, **settings):
        TrTask.__init__(self, tobject, jid, sjid, cmdobject, globaltasklist, **settings)
        self.sqlInserted = False        


    def createTask(self, child, jid, sjid, cmdobject, globaltasklist):
        task = TrSQLTask(child, jid, sjid, cmdobject, globaltasklist, logger=self.logger)
        return task

    def createCmd(self, jid, sjid, tid, cid, cmdobject):
        cmd = TrSQLCmd(jid, sjid, tid, cid, cmdobject, logger=self.logger)
        return cmd
        

    def collectTaskInfo(self, taskinfo):
        if self.sqlInserted: taskinfo.append(self.tid)
        for tid in self.tasklist:
            task = self.tasklist[tid]
            task.collectTaskInfo(taskinfo)

    def processTaskInfo(self, taskinfo):
        if self.tid in taskinfo:
            self.sqlInserted = True
        for tid in self.tasklist:
            task = self.tasklist[tid]
            task.processTaskInfo(taskinfo)

    def processCmdInfo(self, cmdinfo):
        for cid in self.cmdlist:
            cmd = self.cmdlist[cid]
            if cmdinfo.has_key(cmd.cid):
                cmd.scid = cmdinfo[cmd.cid]

    def collectCmdInfo(self, cmdinfo):
        for cid in self.cmdlist:
            cmd = self.cmdlist[cid]
            cmdinfo[cmd.cid]=cmd.scid
    
    
    def saveSQLState(self, sqlObj, doUpdate, sqltimestamp, forceUpdate):
        if doUpdate and self.sqlInserted:
            updateRequired = forceUpdate or (not self.statetime or self.statetime > sqltimestamp)
            if updateRequired:
                sqlObj.TrSQLUpdateTask(self)
        else:
            self.sqlInserted = sqlObj.TrSQLInsertTask(self)

        for tid in self.tasklist:
            task = self.tasklist[tid]
            task.saveSQLState(sqlObj, doUpdate, sqltimestamp, forceUpdate)

        for cid in self.cmdlist:
            cmd = self.cmdlist[cid]
            cmd.saveSQLState(sqlObj, doUpdate, sqltimestamp, forceUpdate)

    def updateSQLJid(self, sjid):
        self.sjid = sjid
        for tid in self.tasklist:
            task = self.tasklist[tid]
            task.updateSQLJid(sjid)

        for cid in self.cmdlist:
            cmd = self.cmdlist[cid]
            cmd.updateSQLJid(sjid)
        
    def debug(self):
        self.logger.debug("Task:sqlinserted: " + str(self.sqlInserted))
        super(TrSQLTask, self).debug()
