#
TrFileRevisionDate = "$DateTime: 2011/04/27 14:11:52 $"
#

"""
    This file is based upon the file "parse_datetime.py"
    which was placed in the public domain by Paul Harrison, 2006.
    It has been modified to parse US formats mm/dd/yy rather than
    the original Australian formats  dd/mm/yy.

    Simple robust time and date parsing.
    
    Note: Follows the Australian standard, dd/mm/yyyy.
          Americans should replace '%d %m %Y' with '%m %d %Y' and '%d %m %y' with '%m %d %y' below.
    
    Routines will either
     - return a date or time
     - return None if the string is empty
     - throw a ValueError
     
    TODO: Handle 1st 2nd 3rd etc

"""

__version__ = '0.1'

import time, datetime

time_formats = ['%H : %M', '%I : %M %p', '%H', '%I %p']

#date_formats_with_year = ['%d %m %Y', '%Y %m %d', '%d %B %Y', '%B %d %Y',
#                                                  '%d %b %Y', '%b %d %Y',
#                          '%d %m %y', '%y %m %d', '%d %B %y', '%B %d %y',
#                                                  '%d %b %y', '%b %d %y']

date_formats_with_year = ['%m %d %Y', '%Y %m %d', '%d %B %Y', '%B %d %Y',
                                                  '%d %b %Y', '%b %d %Y',
                          '%m %d %y', '%y %m %d', '%d %B %y', '%B %d %y',
                                                  '%d %b %y', '%b %d %y']

date_formats_without_year = ['%d %B', '%B %d',
                             '%d %b', '%b %d']

def parse_time(string):
    string = string.strip()
    if not string: return None
    
    for format in time_formats:
        try:
            result = time.strptime(string, format)
            return datetime.time(result.tm_hour, result.tm_min)
        except ValueError:
            pass
            
    raise ValueError()

    
def parse_date(string):
    string = string.strip()
    if not string: return None
    
    string = string.replace('/',' ').replace('-',' ').replace(',',' ')
    
    for format in date_formats_with_year:
        try:
            result = time.strptime(string, format)
            return datetime.datetime(result.tm_year, result.tm_mon, result.tm_mday)
        except ValueError:
            pass

    for format in date_formats_without_year:
        try:
            result = time.strptime(string, format)
            year = datetime.date.today().year
            return datetime.datetime(year, result.tm_mon, result.tm_mday)
        except ValueError:
            pass
            
    raise ValueError()


if __name__ == '__main__':
    pass
