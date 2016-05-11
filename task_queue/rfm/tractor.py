#!/usr/bin/env python
#
TrFileRevisionDate = "$DateTime: 2009/04/23 17:17:43 $"

#
# tractor-spool - Spool a new job into the Tractor job queue.
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


import os
import sys
import platform
import optparse
import datetime
import getpass
import socket

## --------- ##
# version check
if sys.version_info < (2, 5):
    print >>sys.stderr,"Error: tractor-spool requires python 2.5 (or later)\n"
    sys.exit(25)
## --------- ##

sys.path.insert(1, os.path.join(sys.path[0], "blade-modules"))
from TrHttpRPC import TrHttpRPC

## --------------------------------------------------- ##
def Spool (argv):
    '''
    tractor-spool - main - examine options, connect to engine, transfer job
    '''
    appName =        "tractor-spool"
    appVersion =     "TRACTOR_VERSION"
    appProductDate = "TRACTOR_BUILD_DATE"
    appDir = os.path.dirname( os.path.realpath( __file__ ) )

    defaultMtd  = "tractor-engine:80"

    spoolhost = socket.gethostname().split('.')[0] # options can override
    user = getpass.getuser()

    # ------ # 

    if not appProductDate[0].isdigit():
        appProductDate = " ".join(TrFileRevisionDate.split()[1:3])
        appVersion = "dev"

    appBuild = "%s %s (%s)" % (appName, appVersion, appProductDate)

    optparser = optparse.OptionParser(version=appBuild,
                                      usage="%prog [options] JOBFILE...\n"
                                        "%prog [options] --rib RIBFILE...\n"
                                        "%prog [options] --jdelete JOB_ID" )

    optparser.add_option("--priority", dest="priority",
            type="float", default=1.0,
            help="priority of the new job")

    optparser.add_option("--engine", dest="mtdhost",
            type="string", default=defaultMtd,
            help="hostname[:port] of the master tractor daemon, "
                 "default is '"+defaultMtd+"' - usually a DNS alias")

    optparser.add_option("--hname", dest="hname",
            type="string", default=spoolhost,
            help="the origin hostname for this job, used to find the "
                 "'home blade' that will run 'local' Cmds; default is "
                 "the locally-derived hostname")

    optparser.add_option("--user", dest="uname",
            type="string", default=user,
            help="alternate job owner, default is user spooling the job")

    optparser.add_option("--jobcwd", dest="jobcwd",
            type="string", default=trAbsPath(os.getcwd()),
            help="blades will attempt to chdir to the specified directory "
                 "when launching commands from this job; default is simply "
                 "the cwd at time when tractor-spool is run")

    optparser.set_defaults(ribspool=None)
    optparser.add_option("--rib", "-r", dest="ribspool",
            action="store_const", const="rcmd",
            help="treat the flename arguments as RIB files to be rendered; "
                 "a single task tractor job is automatically created to handle "
                 "the rendering (using prman on remote blade)")

    optparser.add_option("--ribs", dest="ribspool",
            action="store_const", const="rcmds",
            help="treat the flename arguments as RIB files to be rendered; "
                 "a  multi-task tractor job is automatically created to handle "
                 "the rendering (using prman on remote blade)")

    optparser.add_option("--nrm", dest="ribspool",
            action="store_const", const="nrm",
            help="a variant of --rib, above, that causes the generated "
                 "tractor job to use netrender on the local blade rather "
                 "than direct rendering with prman on a blade; used when "
                 "the named RIBfile is not accessible from the remote "
                 "blades directly")

    optparser.add_option("--skey", dest="ribservice",
            type="string", default="pixarRender",
            help="used with --rib to change the service key used to "
                 "select matching blades, default: pixarRender")

    optparser.add_option("--jdelete", dest="jdel_id",
            type="string", default=None,
            help="delete the requested job from the queue")

    optparser.set_defaults(loglevel=1)
    optparser.add_option("-v",
            action="store_const", const=2, dest="loglevel",
            help="verbose status")
    optparser.add_option("-q",
            action="store_const", const=0, dest="loglevel",
            help="quiet, no status")

    optparser.add_option("--paused", dest="paused",
            action="store_true", default=False,
            help="submit job in paused mode")

    rc = 0
    xcpt = None

    try:
        options, jobfiles = optparser.parse_args( argv )

        if options.jdel_id:
            if len(jobfiles) > 0:
                optparser.error("too many arguments for jdelete")
                return 1
            else:
                return jobDelete(options)

        if 0 == len(jobfiles):
            optparser.error("no job script specified")
            return 1

        if options.loglevel > 1:
            print "%s\nCopyright (c) 2007-%d Pixar. All rights reserved." \
                    % (appBuild, datetime.datetime.now().year)

        if options.mtdhost != defaultMtd:
            h,n,p = options.mtdhost.partition(":")
            if not p:
                options.mtdhost = h + ':80'

        # paused starting is represented by a negative priority
        # decremented by one. This allows a zero priority to pause
        if options.paused:
            try:
                options.priority = str( -float( options.priority ) -1 )
            except Exception:
                options.priority = "-2"

        # apply --rib handler by default if all files end in ".rib"
        if not options.ribspool and \
            reduce(lambda x, y: x and y,
                    [f.endswith('.rib') for f in jobfiles]):
            options.ribspool = 'rcmds'

        #
        # now spool new jobs
        #
        if options.ribspool:
            rc = createRibRenderJob(jobfiles, options)
            if rc == 0:
                rc, xcpt = jobSpool(jobfiles[0], options)
        else:
            for filename in jobfiles:
                rc, xcpt = jobSpool(filename, options)
                if rc:
                    break

    except KeyboardInterrupt:
        xcpt = "received keyboard interrupt"

    except SystemExit, e:
        rc = e

    except:
        errclass, excobj = sys.exc_info()[:2]
        xcpt = "job spool: %s - %s" % (errclass.__name__, str(excobj))
        rc = 1

    if xcpt:
        return xcpt
    else:
       return rc

## ------------------------------------------------------------- ##

def trAbsPath (path):
    '''
    Generate a canonical path for tractor.  This is an absolute path
    with backslashes flipped forward.  Backslashes have been known to
    cause problems as they flow through system, especially in the 
    Safari javascript interpreter.
    '''
    return os.path.abspath( path ).replace('\\', '/')

## ------------------------------------------------------------- ##

def jobSpool (jobfile, options):
    '''
    Transfer the given job (alfred script) to the central job queue.
    '''

    if options.ribspool:
        alfdata = options.ribjobtxt
    else:
        # usual case, read the alfred jobfile
        f = open(jobfile, "rb")
        alfdata = f.read()
        f.close()

    hdrs = {
        'Content-Type':         'application/tractor-spool',
        'X-Tractor-User':       options.uname,
        'X-Tractor-Spoolhost':  options.hname,
        'X-Tractor-Dir':        options.jobcwd,
        'X-Tractor-Jobfile':    trAbsPath(jobfile),
        'X-Tractor-Priority':   str(options.priority)
    }

    return TrHttpRPC(options.mtdhost,0).Transaction("spool",alfdata,None,hdrs)

## ------------------------------------------------------------- ##

def createRibTask (ribfiles, options):
    single = True if  type(ribfiles) == type ("") else False 

    jtxt = "  Task -title {"
    if single:
        jtxt += ribfiles
    else:
        jtxt += " ".join( [os.path.basename(f) for f in ribfiles] )
    jtxt += "} -cmds {\n"

    if 'nrm' == options.ribspool:
        jtxt += "    Cmd {netrender %H -f -Progress"
    else:
        jtxt += "    RemoteCmd {prman -Progress"

    if single:
        jtxt += ' "' + ribfiles + '"'
    else:
        jtxt += ' "' + '" "'.join(ribfiles) + '"'
    jtxt += '} -service {' + options.ribservice + '} -tags {prman}'
    jtxt += "\n  }\n"  # end of cmds
    return jtxt
    
## ------------------------------------------------------------- ##

def createRibRenderJob (ribfiles, options):
    rc = 0
    jtxt = "##AlfredToDo 3.0\n"
    jtxt += "Job -title {" + os.path.basename(ribfiles[0])
    if len(ribfiles) > 1:
        jtxt += " ..."
    jtxt += "} -subtasks {\n"
    if options.ribspool=="rcmds":
        for f in ribfiles:
            jtxt += createRibTask(f, options)
    else:
        jtxt += createRibTask(ribfiles, options)

    jtxt += "}\n"    # end of job

    options.ribjobtxt = jtxt

    return rc


## ------------------------------------------------------------- ##

def jobDelete (options):
    '''
    Request that a job be deleted from the tractor queue
    '''
    sjid = str( options.jdel_id )

    q = "queue?q=jdelete&jid=" + sjid
    q += "&user=" + options.user
    q += "&hnm=" + options.hname

    rc, msg = TrHttpRPC(options.mtdhost,0).Transaction(q)

    if 0 == rc:
        print "J" + sjid + " delete OK"
    else:
        print msg

    return rc


## ------------------------------------------------------------- ##

if __name__ == "__main__":

    rc = Spool( sys.argv[1:] )

    if 0 != rc:
        sys.exit(rc)

## ------------------------------------------------------------- ##

