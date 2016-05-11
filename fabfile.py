from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

import fabric.exceptions
import pdb

host_list = []
for i in xrange(40, 255):
    host_list.append("172.16.15.{0}".format(i))

env.hosts = host_list #sorted(host_list, reverse=True)

env.user="root"
env.password="centos6"

def get_host_name():
	try:
	    with settings(warn_only=True):	
	        result = run('uname -a', timeout=5, quiet=True)
	    if result.failed and not confirm("Tests failed. Continue anyway?"):
	        abort("Aborting at user request.")
	    # Print host    
	    print("SUCCESS => Host: {0}".format(result.split()[1])) 
	except Exception as e:
		print(e.message)