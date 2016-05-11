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

from TrCmd import TrCmd

## --------------------------------------------------------- ##

class TrSQLCmd(TrCmd):

    def __init__(self, jid, sjid, tid, cid, cmdobject, **settings):
        TrCmd.__init__(self,jid, sjid, tid, cid, cmdobject, **settings)

        
    def saveSQLState(self, sqlObj, doUpdate, sqltimestamp, forceUpdate):
        if doUpdate and self.scid:
            updateRequired = forceUpdate \
                or (not self.statetime or self.statetime > sqltimestamp)
            if updateRequired:
                sqlObj.TrSQLUpdateCmd(self)
        else:
            self.scid = sqlObj.TrSQLInsertCmd(self)            

    def updateSQLJid(self, sjid):
        self.sjid = sjid

