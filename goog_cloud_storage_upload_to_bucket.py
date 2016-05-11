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

dump_file_glob = "/tmp/inventory_db*"
newest_dump_file = max(glob.iglob(dump_file_glob), key=os.path.getctime)
dump_file_basename = os.path.basename(newest_dump_file)

for bucket in (sys.argv[1:]):
    with open(newest_dump_file, 'r') as localfile:
        uri = boto.storage_uri(bucket + '/' + dump_file_basename, GOOGLE_STORAGE)
        uri.new_key().set_contents_from_file(localfile)

        print 'Successfully created "%s/%s"' % (uri.bucket_name, uri.object_name)



