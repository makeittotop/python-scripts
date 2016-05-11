#!/usr/bin/env python
#

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
import optparse
import logging
import logging.handlers
import errno
import traceback
import socket
import select
import getpass
import re
import Queue
import threading
import time
import os

## ------------------------------------------------------------- ##

filepath = sys.path[0]
newpath = os.path.join(filepath, "..", "python-modules")
sys.path.insert(0, newpath)
newpath = os.path.join(filepath, "..", "blade")
sys.path.insert(1, newpath)

#from TrHttpRPC import TrHttpRPC
from tractor.base.TrHttpRPC import TrHttpRPC

## ------------------------------------------------------------- ##
def retryApproval(jid, tid, opts, logger):
    
    response = True
    if jid in retryDict:
        jentry = retryDict[jid]
        if tid in jentry:
            count = jentry[tid]
            if count >= opts.tretry: 
                response = False
            else: 
                jentry[tid] = jentry[tid] + 1
        else:
            jentry[tid] = 1
    else:
        retryDict[jid] = {tid : 1}
     
    jcount = 0
    if jid in retryDict:
        jentry = retryDict[jid]
        for tid in jentry:
            jcount += jentry[tid]

    if response and jcount > opts.jretry: response = False
    
    return response


## ------------------------------------------------------------- ##
def processTractorJobs (opts, logger, appname, appvers, appdate):
    
    global password
    errsleep=1
    minerrsleep=1
    maxerrsleep=60
    
    client = opts.user  # to register this observer, not job filter
    host,x,port = opts.monitor.partition(':')

    lmthdr = {
        'User-Agent': "Pixar-%s/%s (%s)" % (appname, appvers, appdate),
        'X-Tractor-Blade': "0"
    }
    xheaders = {
        'Host': "%s:%s" % (host, port),
        'Cookie': "TractorUser=%s" % client
    }

    
    if opts.configfile:
        # try to read and eval the file
        # if the authorization data ain't there the except
        # will handle it
        try:
            f=open(opts.configfile, "r")
        except:
            logger.error("unable to locate config file: %s", 
                opts.configfile)
            raise
        try:
            data=f.read()
            f.close()
            # the config file is supposed to contain at a minumum user and password
            # info to log into the monitor. raises an exception if not defined
            configdict = eval(data)
            tractordict =  configdict["tractorconfig"]
            client = tractordict["user"]
            password = tractordict["passwd"]
            
            # it may also contain other config information like monitor and port
            # this we want to be careful and not raise an exception if they do not 
            # exist.  These entries are not required
            if "monitor" in tractordict:
                host,x,port = tractordict["monitor"].partition(':')
            if "port" in tractordict:
                port = tractordict["port"]
        except:
            logger.error("config file contains invalid data: %s", opts.configfile)
            raise
            
        
    connector = TrHttpRPC(host, int(port), logger, lmthdr, timeout=3600)
    passwordRequired = connector.PasswordRequired()
    if passwordRequired and not password:
        # password is global, so that it will be remembered if connection fails
        # or is restarted
        if opts.passwd:  password = opts.passwd
        else: password = getpass.getpass("Enter password for %s: " % client)
    try:
        data =  connector.Login(client, password)
    except Exception, e:
        errclass, excobj = sys.exc_info()[:2]
        logger.error("%s - %s" % (errclass.__name__, str(excobj)))        
        raise RuntimeError()
        
    tsid = data['tsid']
    if tsid == None:
        logger.error("unable to log in user: %s" % client)
        raise Exception("unable to log in user: %s" % client)    
    
    logger.info("login successful for %s:%s" %(client, str(tsid)))

    q = "q=subscribe&tsid="+tsid + "&jids=0"

    snames = {
        'A': "Active", 'B': "Blocked", 'C': "Cleaning",
        'D': "Done",   'E': "Error"
    }

    #
    # the subscription / observer loop
    #
    while 1:
        try:
            err, data = connector.Transaction("monitor?"+q, None, "subtest", xheaders)
            if err:
                if err == -1:
                    # no real error, query timed out, didn't produce data
                    logger.log(logging.TRACE, "code="+str(err)+" - "+repr(data))
                    continue
                elif err in [61, 400, 404, 424]:
                    logger.error("code="+str(err)+" - "+data)
                    raise RuntimeError(err)
                else:
                    logger.error("code="+str(err)+" - "+data)
                    time.sleep(errsleep)
                    errsleep = errsleep * 2
                    errsleep = min(errsleep, maxerrsleep)
                    logger.warning("retrying connection to engine")                
            else:
                errsleep=minerrsleep
                for msg in data['mbox']:
                    logger.debug(msg)
                    if 'j' == msg[0]:
                        if re.search('#', msg[1]): continue

                    elif 'c' == msg[0]:
                        jid = msg[1]
                        tid = msg[2];
                        cid = msg[3];
                        status = msg[4];
                        user = msg[12];
                        if 'E' == status and tid > 0 and cid > 0:
                            if retryApproval(jid, tid, opts, logger):
                                command="queue?q=tretry&jid=%d&tid=%d&owner=%s&tsid=%s" \
                                    % (jid, tid, user, tsid)
                                    
                                logger.info("Restart task: %d on job: %d" % (tid, jid))
                                logger.debug(command)
                                err, data = connector.Transaction(command, None, "subtest", xheaders)

                    else:
                        pass

        except KeyboardInterrupt:
            logger.critical("keyboard interrupt")
            q = "q=logout&user="+client+"&tsid="+tsid
            err, data = connector.Transaction("monitor?"+q, None, "logout", xheaders)
            logger.info("code="+str(err)+" - "+repr(data))
            raise KeyboardInterrupt


## ------------------------------------------------------------- ##
def monitorTractorJobs (opts, logger, appname, appvers, appdate):
    errsleep=1
    minerrsleep=1
    maxerrsleep=60
    
    while 1:
        try:
            processTractorJobs (opts, logger, appname, appvers, appdate)
        except KeyboardInterrupt:
            logger.critical("keyboard interrupt")
            return
        except RuntimeError, e:
            time.sleep(errsleep)
            errsleep = errsleep * 2
            errsleep = min(errsleep, maxerrsleep)
            logger.warning("Login error, retrying")
        except Exception, e:
            errclass, excobj = sys.exc_info()[:2]
            logger.error("%s - %s" % (errclass.__name__, str(excobj)))
            return

    
## ------------------------------------------------------------- ##

def main():
        
    global retryDict, password
    
    retryDict = {}
    password = None
    
    # Note:  this version requires TrHttpRPC from tractor 1.5
    # which supports the Login() and PasswordRequired() methods
    
    appName =        "jobMonitor"
    appVersion =     "2.0"
    appProductDate = "2011-Dec-6"

    # first, add a new log level to logging module
    logging.TRACE=5
    logging.addLevelName(5, 'TRACE')


    # portability fix for windows
    if not hasattr(errno, "ERROR_ALREADY_EXISTS"):
        errno.ERROR_ALREADY_EXISTS = 183

    desc = """This program monitors subscriptions messages from 
the tractor monitor, and watches for jobs that are exiting with
an error status.  It then retries the tasks until either the task
maximum retry or job total retries has been exhausted"""

    optparser = optparse.OptionParser(description=desc)

    optparser.add_option("-m", "--monitor", dest="monitor",
            type="string", default="tractor-monitor:1503",
            help="tractor monitor:port [default: %default]")

    user = getpass.getuser()

    optparser.add_option("-u", "--user", dest="user",
            type="string", default=user,
            help="tractor user to login [default: %default]")

    optparser.add_option("-p", "--passwd", dest="passwd",
            type="string", default=None,
            help="password for tractor user to login [default: %default]")

    optparser.add_option("--configfile", dest="configfile",
            type="string", default=None,
            help="JSON file containing login and password data"
            " [default: %default]")

    optparser.add_option("--tretry", dest="tretry",
            type="int", default="3",
            help="Number of times to retry an error task [default: %default]")
            
    optparser.add_option("--jretry", dest="jretry",
            type="int", default="5",
            help="Number of times to retry an error in a single job [default: %default]")
            
    optparser.set_defaults(loglevel=logging.WARNING)
    group = optparse.OptionGroup(optparser, "Logging Options",
    "Defines logging level and logfile. [default: WARNING]")

    group.add_option("-v", "--verbose",
            action="store_const", const=logging.INFO,  dest="loglevel",
            help="log level Info and above")
    group.add_option("--debug",
            action="store_const", const=logging.DEBUG, dest="loglevel",
            help="log level Debug and above")
    group.add_option("--trace",
            action="store_const", const=logging.TRACE, dest="loglevel",
            help="log level Trace and above")
    group.add_option("--warning",
            action="store_const", const=logging.WARNING, dest="loglevel",
            help="log level Warning and above, the default")
    group.add_option("-q", "--quiet",
            action="store_const", const=logging.CRITICAL, dest="loglevel",
            help="log level Critical only")

    group.add_option("--logfile", dest="logfile",
            type="string", default=None,
            help="Local logfile for debugging [default: %default]")
            
    optparser.add_option_group(group)
    (options,args) = optparser.parse_args()

    logger = logging.getLogger("jobMonitor")
    logger.setLevel(options.loglevel)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch = logging.StreamHandler()

    if (options.logfile):
        ch = logging.FileHandler(options.logfile)

    ch.setLevel(options.loglevel)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    monitorTractorJobs (options, logger, appName, appVersion, appProductDate)


## ------------------------------------------------------------- ##
if __name__ == "__main__":
    main()
