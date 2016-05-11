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

## --------------------------------------------------------- ##

class TrCmd(object):

    def __init__(self, jid, sjid, tid, cid, cmdobject, **settings):
        if settings.has_key("logger"):
            self.logger = settings["logger"]
        else:
            self.logger = logging.getLogger("tractor")


        self.jid            =   jid
        self.sjid           =   sjid
        self.tid            =   tid
        self.cid            =   cid
        self.scid           =   None    # SQL cid for updates
        self.commandline    =   cmdobject['argv']
        self.keylist        =   cmdobject['envkey'] if cmdobject.has_key('envkey') else None
        self.taglist        =   cmdobject['tags'] if cmdobject.has_key('tags') else None
        self.service        =   cmdobject['service'] if cmdobject.has_key('service') else None
        self.slots          =   None
        self.statetime      =   None
        self.starttime      =   None
        self.endtime        =   None
        self.status         =   'U'
        
    def updateStatus(self, timestamp, state, host):
        self.statetime = datetime.fromtimestamp(timestamp)
        if state == 'A': self.starttime = self.statetime
        if state == 'D': self.endtime = self.statetime
        if state == 'E': self.endtime = self.statetime
        self.status = state
        self.slots = host
    

    def debug(self):
        self.logger.debug("Cmd:jid: " + str(self.jid))
        self.logger.debug("Cmd:sjid: " + str(self.sjid))
        self.logger.debug("Cmd:tid: " + str(self.tid))
        self.logger.debug("Cmd:cid: " + str(self.cid))
        self.logger.debug("Cmd:scid: " + str(self.scid))
        self.logger.debug("Cmd:status: " + str(self.status))
        self.logger.debug("Cmd:commandline: " + str(self.commandline))
        self.logger.debug("Cmd:keylist: " + str(self.keylist))
        self.logger.debug("Cmd:taglist: " + str(self.taglist))
        self.logger.debug("Cmd:service: " + str(self.service))
        self.logger.debug("Cmd:statetime: " + str(self.statetime))
        self.logger.debug("Cmd:starttime: " + str(self.starttime))
        self.logger.debug("Cmd:endtime: " + str(self.endtime))
        
    
        
        
