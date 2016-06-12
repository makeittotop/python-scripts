#!/usr/bin/env python

import pycurl
import json
import iso8601
import datetime
from StringIO import StringIO
import re

class MyData(object):                                                                                                             
    created_at=''                                                                                                                 
    updated_at = ''                                                                                                               
    login = ''                                                                                                                    
    id = ''                                                                                                                       
    description = ''                                                                                                              
    filename = ''                                                                                                                 
    _matter = ''
    def __init__(self, d):                                                                                                        
      self.created_at=iso8601.parse_date(d.get('created_at'))                                                                     
      self.updated_at=iso8601.parse_date(d.get('updated_at'))                                                                     
      self.login=d.get('owner').get('login')                                                                                      
      self.id=d.get('id')                                                                                                         
      self.description=d.get('description').encode('utf-8').title()                                                                               
      self.filename=d.get('files').keys()[0].encode('utf-8').title()                                                                              
    _matter= '''---
layout: single                                                                                                              
title: {0}                                                                                                                       
date: {1}                                                                                                                        
categories: Linux                                                                                                                
---                                                                                                                              

{{% gist {2}/{3} %}}                                                                                                           
'''                                                                                                                              
    def create_matter(self): 
        if not re.search('gistfile', self.filename, re.IGNORECASE):
            self.matter = self._matter.format(self.filename.replace("_", " ").replace("-", " "), self.created_at, self.login, self.id)                                         
        else:
            self.matter = self._matter.format(self.description.replace("_", " ").replace("-", " "), self.created_at, self.login, self.id)    

    def print_matter(self):                                                                                                       
        self.create_matter()                                                                                                      
        self.file_name()                                                                                                          
        with open(self.fh, "w") as h:                                                                                             
            print >> h, self.matter                                                                                               

    def file_name(self):                                                                                                          
        if not re.search('gistfile', self.filename, re.IGNORECASE):
            self.fh = str(self.created_at.strftime("%Y-%m-%d")) + "-" + str(self.filename.replace(" ", "-").replace("_", "-")) + ".markdown"
        else:
            self.fh = str(self.created_at.strftime("%Y-%m-%d")) + "-" + str(self.description.replace(" ", "-").replace("_", "-")) + ".markdown"    

for i in range(10):                                                                                                                     
    buffer = StringIO()                                                                                                                 
    pycurl_connect = pycurl.Curl()                                                                                                      
    #pycurl_connect.setopt(pycurl.HTTPHEADER, ['Authorization: token ******************************',])
    print i+1; pycurl_connect.setopt(pycurl.URL, "https://api.github.com/users/makeittotop/gists?page={0}".format(i+1))                 
    pycurl_connect.setopt(pycurl_connect.WRITEFUNCTION, buffer.write)                                                                   
    pycurl_connect.perform()                                                                                                            
    pycurl_connect.close()                                                                                                              
    body = buffer.getvalue()                                                                                                            
    data = json.loads(body)                                                                                                             
    mlist = []                                                                                                                          
    for d in data:                                                                                                                      
        mlist.append(MyData(d))                                                                                                         
    for item in mlist:                                                                                                                  
        item.print_matter(); print item.fh                                                                                              
    print "--- page done ---" 
