#!/usr/bin/env python

import boto
import gcs_oauth2_boto_plugin
import os
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

uri = boto.storage_uri('', GOOGLE_STORAGE)
# If the default project is defined, call get_all_buckets() without arguments.
for bucket in uri.get_all_buckets(headers=header_values):
      print bucket.name



