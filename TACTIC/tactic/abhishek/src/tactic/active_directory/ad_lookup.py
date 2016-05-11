###########################################################
#
# Copyright (c) 2005-2009, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#

__all__ = ['ADLookup', 'ADException']


import os

from pyasm.common import TacticException


class ADException(TacticException):
    pass

ERROR = ""
try:
    import win32security, pywintypes
    import active_directory
except ImportError, e:
    if os.name != 'nt':
        ERROR = "Active directory libraries only work on a Windows platform"
    else:
        ERROR = 'Cannot import Win32 modules'



class ADLookup(object):

    def __init__(my):
        my.debug_flag= False
        my.domain=""
        my.filter=""
        my.object=""

        if ERROR:
            raise ADException(ERROR)


    def set_domain(my, domain):
        my.domain = domain
        my.debug("Setting domain to %s" % my.domain)

    def set_debug(my, bool):
        my.debug_flag=True

    def set_ldap_string(my, ldapstring):
        my.ldap_string=ldapstring
    
    def get_root(my):
        return active_directory.root()
    
    def set_object(my, object):
        my.object=object
    
    def set_filter(my, filter):
        my.filter=filter
    
    def debug(my, message):
        if my.debug_flag:
            print message


    def lookup_attr(my, username, attr):
        user=active_directory.find_user(username)
        print user.attr
        return user.attr


    def lookup_name(my, username):
        user=active_directory.find_user(username)
        #print user.dump
        #x=user.properties
        #print x.cn
        print user.cn
        return user.cn


    def lookup_user(my, username):
        user=active_directory.find_user(username)
        return user





import sys, getopt

def usage():
    print "ADS lookup tool"
    print "Usage: ad_lookup.py [Option]"
    print "Check for ADS data"
    print ""
    print "-u <name>            Look up the username 'name'"
    print "-o <objectname>      objectname - ex. \"displayName\""
    print "-f <filter>          filter - ex. \"objectName=person\""
    print "-h, --help           Display this message, and exit"
    print "-i                   lookup root info"
    print "-r                   execute the lookup"      
    print "-d                   Debug messages"
    print ""

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "o:f:u:hdcir", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    #try:
    if len(opts) > 0:
        ads = ADLookup()
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt == '-o':
                ads.set_object(arg)
            elif opt == '-f':
                ads.set_filter(arg)
            elif opt == '-i':
                print ads.get_root()
            elif opt == '-d':
                ads.set_debug(True)
            elif opt == '-r':
                ads.lookup()
            elif opt == '-u':
                ads.lookup_name(arg)
            else:
                usage()
                sys.exit()
    else:
        print ("Try 'ad_lookup.py -h' for more information.")

if __name__ == '__main__':
    main(sys.argv[1:])
