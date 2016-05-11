#!/usr/bin/env python

import boto
import gcs_oauth2_boto_plugin
import os, sys
import shutil
import StringIO
import tempfile
import time

# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

# Your project ID can be found at https://console.developers.google.com/
# If there is no domain for your project, then project_id = 'YOUR_PROJECT'
project_id = 'iron-atom-89306'

header_values = {"x-goog-project-id": project_id}

# If the default project is defined, call get_all_buckets() without arguments.
bucket = sys.argv[1]

for bucket in (sys.argv[1:]):
    uri = boto.storage_uri(bucket, GOOGLE_STORAGE)
    try:
        uri.create_bucket(headers=header_values)
        print 'Successfully created bucket "%s"' % bucket
    except boto.exception.StorageCreateError, e:
        print 'Failed to create bucket:', e.message 



