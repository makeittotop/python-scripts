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
import types

from TrJob import TrJob

TrModeObject = 1
TrModeInfo = 2

## --------------------------------------------------------- ##
class TrContext(object):

    
    def __init__(self, **settings):
        
        self.logger     = None
        self.rootdir    = "/var/spool/tractor"
        self.jobclass   = TrJob
        self.host       = "localhost"
        self.mode       = TrModeInfo
        
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

        if settings.has_key("rootdir"):
            self.rootdir = settings["rootdir"]
        if settings.has_key("jobclass"):
            self.jobclass = settings["jobclass"]
        if settings.has_key("host"):
            self.host = settings["host"]
        if settings.has_key("mode"):
            self.mode = settings["mode"]
            
        self.validhost = validateHostname(self.host)
        if not self.validhost:
            self.logger.error("TrContext does not currently support remote machine access")
            
                                                   
    def FindJob(self, **settings):
        """a generator returning a list of job info (jid, user, jobdir) 
        or job objects via an iterator function, depending upon mode"""

        if not self.validhost: return
        user = None
        minspooltime = None
        maxspooltime = None
        mode = self.mode
        
        if settings.has_key('user'):
            user = settings['user']

        if settings.has_key('mode'):
            mode = settings['mode']
                        
        if settings.has_key('spooltime'):
            spooltime = settings['spooltime']
            if spooltime:
                if type(spooltime) == types.TupleType:
                    minspooltime, maxspooltime = spooltime
                else:
                    minspooltime = spooltime

        if minspooltime:
            minbasespooltime = datetime(minspooltime.year, minspooltime.month, 1)
        if maxspooltime:
            maxbasespooltime = datetime(maxspooltime.year, maxspooltime.month, 1)
        
        rootSlashCount = self.rootdir.count(os.sep)
        gen = os.walk(os.path.join(self.rootdir, "jobs"))
        for root,dirs,files in gen:
            dirs.sort(reverse=True)
            slashCount = root.count(os.sep)
            levels = slashCount - rootSlashCount
            
            if levels == 2:             #YYYY-MM
                l = root.split(os.sep)
                year, month = l[-1].split("-")
                year = int(year)
                month = int(month)
                day = 1
                dirtime = datetime(year, month, day)

                if minspooltime:
                    if dirtime < minbasespooltime:
                        del dirs[:]
                        continue

                if maxspooltime:
                    if dirtime > maxbasespooltime:
                        del dirs[:]
                        continue   

            elif levels == 3:       #DD
                l = root.split(os.sep) 
                day = int(l[-1])

                if minspooltime:
                    mintime = datetime(year, month, day)
                    if mintime < minspooltime:
                        del dirs[:]
                        continue

                if maxspooltime:
                    maxtime = datetime(year, month, day)
                    if maxtime > maxspooltime:
                        del dirs[:]
                        continue
                                   
            elif levels == 4:
                l = root.split(os.sep)
                userdir = l[-1]
                if user and  user != userdir:
                    del dirs[:]
                    continue

            elif levels == 5:
                l = root.split(os.sep)
                jid = l[-1]
                try:
                    jid = int(jid)
                except:
                    continue
                if mode == TrModeInfo:
                    yield jid,userdir,root
                elif mode == TrModeObject:
                    job = self.job(userdir, jid, jobdir=root, mode=mode)
                    yield job
                                                   

    def job(self, user, jid, **settings):
        if not self.validhost: return None
        
        args = {"logger": self.logger, "rootdir": self.rootdir}
        args.update(settings)
        job = self.jobclass(user, jid, **args)
        return job
        
    def debug(self):
        self.logger.debug("rootdir: " + self.rootdir)
        self.logger.debug("jobclass: " + repr(self.jobclass))
        self.logger.debug("host: " + str(self.host))
        self.logger.debug("validhost: " + str(self.validhost))
        self.logger.debug("mode: " + str(self.mode))
                


        
## -------------------Support Functions -------------------------------------- ##
def validateHostname(name):
    """TrContext functions currently only support local operations.  
       Make sure that either host is "localhost", or that supplied name
       resolves to this host"""
       
    if name == "localhost": return True
    import socket
    
    hostname,aliases,address=socket.gethostbyname_ex(socket.gethostname())
    if name == hostname: return True
    if name in aliases: return True
    return False
    
               
