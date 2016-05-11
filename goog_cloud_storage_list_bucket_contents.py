#!/usr/bin/env python

import boto
import gcs_oauth2_boto_plugin
import os, sys, glob

# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

# Your project ID can be found at https://console.developers.google.com/
# If there is no domain for your project, then project_id = 'YOUR_PROJECT'
project_id = 'iron-atom-89306'

header_values = {"x-goog-project-id": project_id}

for bucket in (sys.argv[1:]):
    uri = boto.storage_uri(bucket, GOOGLE_STORAGE)
    for obj in uri.get_bucket():
        print '%s://%s/%s' % (uri.scheme, uri.bucket_name, obj.name)
        print '  "%s"' % obj.get_contents_as_string()



