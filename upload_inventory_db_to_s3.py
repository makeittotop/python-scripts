#!/usr/bin/env python

import sys, os, glob

# amazon web services api
import boto

AWS_ACCESS_KEY_ID='AKIAIVZLHF74OTT3U4EA'
AWS_SECRET_ACCESS_KEY='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'

def main():
    dump_file_glob = "/tmp/inventory_db*"

    newest_dump_file = max(glob.iglob(dump_file_glob), key=os.path.getctime)

    dump_file_basename = os.path.basename(newest_dump_file)

    # Form a connection with the s3
    conn = boto.connect_s3(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Get the relevant bucket
    bucket = conn.get_bucket('com.amazon.s3.abhishekpareek1983.barajoun.inventory_db')

    # Make a new file
    k = boto.s3.key.Key(bucket)
    k.key = os.path.basename(dump_file_basename)

    # Set the contents to the source file
    k.set_contents_from_filename(newest_dump_file, replace=False)

    print >>sys.stderr, "File {0} successfully uploaded to s3!".format(newest_dump_file)

main()