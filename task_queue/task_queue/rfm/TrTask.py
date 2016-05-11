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

from TrCmd  import TrCmd

## --------------------------------------------------------- ##
class TrTask(object):

    def __init__(self, tobject, jid, sjid, cmdobject, globaltasklist, **settings):
        if settings.has_key("logger"):
            self.logger = settings["logger"]
        else:
            self.logger = logging.getLogger("tractor")

        self.tasklist       =   {}
        self.cmdlist        =   {}
        self.jid            =   jid
        self.sjid           =   sjid
        self.tid            =   tobject['data']['tid']
        self.title          =   tobject['data']['title']
        self.state          =   'U'
        self.statetime      =   None
        self.readytime      =   None
        globaltasklist[self.tid] = self
        
        if tobject['data'].has_key('cids'):
            for cid in tobject['data']['cids']:
                cnum = "C%d" % cid
                cmd = self.createCmd(self.jid, self.sjid, self.tid, cid, cmdobject[cnum])
                self.cmdlist[cid] = cmd

        for child in tobject['children']:
            task = self.createTask(child, self.jid, self.sjid, cmdobject, globaltasklist)
            tid = child['data']['tid']
            self.tasklist[tid] = task                  


        
    def createTask(self, child, jid, sjid, cmdobject, globaltasklist):
        task = TrTask(child, jid, sjid, cmdobject, globaltasklist, logger=self.logger)
        return task

    def createCmd(self, jid, sjid, tid, cid, cmdobject):
        cmd = TrCmd(jid, sjid, tid, cid, cmdobject, logger=self.logger)
        return cmd
        
    def updateStatus(self, cid, timestamp, state, host):
        self.statetime = datetime.fromtimestamp(timestamp)
        self.state = state

        if cid == 0:  return    # this is a task level only
        if self.cmdlist.has_key(cid):
            cmd = self.cmdlist[cid]
            cmd.updateStatus(timestamp, state, host)
    
    def buildTaskMap(self, taskstring):
        taskstring += "{%ld" % self.tid
        for tid in self.tasklist:
            task = self.tasklist[tid]
            taskstring = task.buildTaskMap(taskstring)
        taskstring += "}"
        return taskstring

    
    def debug(self):
        self.logger.debug("Task:jid: " + str(self.jid))
        self.logger.debug("Task:sjid: " + str(self.sjid))
        self.logger.debug("Task:tid: " + str(self.tid))
        self.logger.debug("Task:title: " + str(self.title))
        self.logger.debug("Task:state: " + str(self.state))
        self.logger.debug("Task:statetime: " + str(self.statetime))
        
        for tid in self.tasklist:
            task = self.tasklist[tid]
            task.debug()

        for cid in self.cmdlist:
            cmd = self.cmdlist[cid]
            cmd.debug()

    
