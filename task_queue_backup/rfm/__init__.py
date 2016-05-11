#
# ------------------------------------------------------------------------------
#
# Copyright (c) 2009 Pixar Animation Studios. All rights reserved.
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
#
# Pixar
# 1200 Park Ave
# Emeryville CA 94608
#
# ------------------------------------------------------------------------------
#
# rfm/__init__.py $Revision: #9 $
#   base-level python module loaded when RfM is loaded.

import imp

Version = None
(FATAL,ERROR,WARNING,NOTICE,INFO,COPIOUS,DEBUG,TRACE,SPEWAGE) = \
                                                        (0,1,2,3,4,5,6,7,8)
Verbosity = NOTICE
s_msglevels = ["FATAL", "ERROR", "WARNING", "NOTICE", 
               "INFO", "COPIOUS", "DEBUG", "TRACE", "SPEWAGE"]

def _bootstrap(version, verbosity):
    """ Initializes _rfm python-side support, called from c-side. """
    Version = version
    Verbosity = s_msglevels.index(verbosity)
    Log(DEBUG, "bootstrapping " + version)

    importXgen()
    
def importXgen():
    # Attempt to load xgen module.
    # Note: It seems we can't do this based on whether xgenToolkit plugin
    # is loaded, because it doesn't get loaded when mayapy is launched to
    # export an xgen archive (xarc), for which we register an export callback.
    try:
        import rfm.xgen
        rfm.xgen.initialize()
        Log(DEBUG, "loading xgen module")
    except:
        Log(DEBUG, "couldn't import xgen module")

def Log(level, str):
    """ Displays a message if is sufficiently important """
    if level <= Verbosity:
        import maya.OpenMaya
        import time
        datestr = time.asctime()
        levstr = s_msglevels[level]
        errstr = "%s rfm %s: %s" % (datestr, levstr, str)
        if level <= ERROR:
            maya.OpenMaya.MGlobal.displayError(errstr)
        elif level == WARNING:
            maya.OpenMaya.MGlobal.displayWarning(errstr)
        else:
            maya.OpenMaya.MGlobal.displayInfo(errstr)

def Warning(msg):
    Log(WARNING, msg)

def Error(msg):
    Log(ERROR, msg)

def Notice(msg):
    Log(NOTICE, msg)

def Info(msg):
    Log(INFO, msg)

