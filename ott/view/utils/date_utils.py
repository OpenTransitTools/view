import logging
log = logging.getLogger(__file__)

import datetime
import time
from calendar import monthrange

def get_local_time():
    return time.localtime()

def get_local_date():
    return datetime.date.today()

def get_time_info(tm=None):
    ''' gets a dict with a few params based on input date-time object
    '''
    if tm is None:
        tm = get_local_time()
    ret_val = {
        'hour'    : int(time.strftime('%I', tm).strip('0')),
        'minute'  : int(time.strftime('%M', tm)), 
        'is_am'   : time.strftime('%p', tm) == 'AM'
    }
    return ret_val


def get_day_info(dt=None):
    ''' gets a dict with a few params based on input date-time object
    '''
    if dt is None:
        dt = get_local_date()

    st,end=monthrange(dt.year, dt.month)
    ret_val = {
        'year'    : dt.year,
        'month'   : dt.month,
        'm_abbrv' : dt.strftime("%b"),
        'm_name'  : dt.strftime("%B"),
        'numdays' : end,
        'day'     : dt.day
    }
    return ret_val


def set_date(dt=None, month=None, day=None, year=None):
    ''' return a datetime object, setting new month & day ranges
    '''
    if dt is None:
        dt = datetime.date.today()

    ret_val = dt
    try:
        if not year : year  = dt.year
        if not month: month = dt.month
        if not day  : day   = dt.day
        ret_val = dt.replace(year, month, day)
    except:
        pass
    return ret_val

def pretty_date(dt=None, fmt='%A, %B %d, %Y'):
    if dt is None:
        dt = datetime.date.today()
    return dt.strftime(fmt)

def make_tab_obj(name, uri=None, date=None, append=None):
    ''' for the date tab on the stop schedule page, we expect an object that has a name and a url
        this method builds that structure, and most importantly, the url for those tabs
    '''

    ret_val = {}

    # put the name of the tab first (and strip off any leading / trailing ZEROs if the name is a date)
    ret_val["name"] = name.lstrip('0').replace('/0','/')

    # next give the tab object a URL ... date is broken up into month and day parts 
    if uri:
        month = ""
        day = ""
        if date:
            month = "&month={0}".format(date.month)
            day = "&day={0}".format(date.day)
        ret_val["url"] = "{0}{1}{2}".format(uri, month, day)
        if append:
            ret_val["url"] = "{0}&{1}".format(ret_val["url"], append)

    return ret_val

