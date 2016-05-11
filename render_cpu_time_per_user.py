#!/usr/bin/env python

import csv
import os, sys
import datetime
import calendar
import math

sys.path.append("/opt/pixar/Tractor-2.0/lib/python2.7/site-packages/")
import tractor.api.query as tq


try:
    arg = sys.argv[1:][0]
except IndexError:
    print >>sys.stderr, "Usage: <script> '<month>-<year>' (e.g. mar-2015)"
    sys.exit(-1)

(month, year) = arg.split("-")

if month.title() not in list(calendar.month_name) and month.title() not in list(calendar.month_abbr):
    print >>sys.stderr, "Wrong Month - {0}".format(month)
    sys.exit(-1)

try:
    month_index =  list(calendar.month_abbr).index(month.title())
except ValueError:
    month_index =  list(calendar.month_name).index(month.title())

year = int(year)
(_, month_range) = calendar.monthrange(year, month_index)

stop_time_start = datetime.datetime(int(year), month_index, 1)
stop_time_end = datetime.datetime(int(year), month_index, month_range, 23, 59, 59)

#print stop_time_start, stop_time_end

query_string = "stoptime>'{0}' and stoptime<'{1}' and numtasks=numdone".format(stop_time_start, stop_time_end)

month_jobs = tq.jobs(query_string, sortby=['stoptime'], archive=True)

if not month_jobs:
    print >>sys.stderr, "No data found for {0}-{1}!".format(month, year)
    sys.exit(-1)

job_list = dict()

cpu_usage_data_per_user = dict()

for job in month_jobs:
     if not job_list.has_key(job['owner']):
         job_list[job['owner']] = []
     job_list[job['owner']].append(job)

for user in job_list:
    elapsed_month_tot = 0
    for job in job_list[user]:
        invocations_job = tq.invocations('jid={0}'.format(job['jid']), archive=True)

        elapsedapp_tot = 0
        elapsedsys_tot = 0
        for invocation in invocations_job:
            elapsedapp_tot += invocation['elapsedapp']
            elapsedsys_tot += invocation['elapsedsys']

        elapsed_tot = elapsedapp_tot + elapsedsys_tot
        elapsed_month_tot += elapsed_tot

    cpu_usage_data_per_user[user]=elapsed_month_tot

csv_file = '/root/render_data/{0}-{1}-aggr.csv'.format(month, year)
with open(csv_file, "wb") as file:
    csvwriter = csv.writer(file, dialect='excel')

    row_header = [
        "User", 'Total CPU Time - Seconds', 'Total CPU time - Human Readable'
    ]
    csvwriter.writerow(row_header)

    for user in cpu_usage_data_per_user:
        row_data = [
            user,
            math.ceil(cpu_usage_data_per_user[user]), 
            str(datetime.timedelta(seconds=math.ceil(cpu_usage_data_per_user[user])))
        ]

        csvwriter.writerow(row_data)

        blank_data = [
            '', '', '', '', ''
        ]
        csvwriter.writerow(blank_data)



"""
for user in cpu_usage_data_per_user:
    print user, "jid", "total elapsed time in seconds", "total elapsed time - human readable"
    for data in cpu_usage_data_per_user[user]:
        print(data['jid'], math.ceil(data['elapsed_tot']), str(datetime.timedelta(seconds=math.ceil(data['elapsed_tot']))))
    print "\n"
"""

'''
for job in month_jobs:
    if not job_list.has_key(job['owner']):
        job_list[job['owner']] = []

    job_list[job['owner']].append(job)




    print(job['jid'])
    print(job['spooltime'])
    print(job['starttime'])
    print(job['stoptime'])   
'''      