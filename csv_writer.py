#!/usr/bin/env python

import csv
with open('/home/abhishek/dev/python/test.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')

    data = [['Employee No','Employee Name','Job Desription','Salary'], ['123453','Jack','CEO','12000'], ['453124','Jane','Director','25000'], ['4568354','Sally','Marketing','68000'], ['684535','Harry','Sales','56000']]


    for item in data:
        spamwriter.writerow(item)
