#!/usr/bin/env python

import sys
sys.path.append('/usr/local/bin')

import s3stat

class MyS3Stat(s3stat.S3Stat):

    def process_results(self, json):
        print json

    def process_error(self, exception, data=None):
        print data
        raise exception

mytask = MyS3Stat(bucket, log_path, for_date, ('AKIAIEC2Q4ZWME7WPOSQ', '0PdvroSpHuzROeuIrEXYMiGgKL+Mwur9s9HzsUGF'))
mytask.run()
