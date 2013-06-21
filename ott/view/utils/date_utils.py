import logging
log = logging.getLogger(__file__)

import datetime
import time
from calendar import monthrange


def get_local_time():
    return time.localtime()

def get_local_date():
    return datetime.date.today()

def get_time_info(tm=get_local_time()):
    ''' gets a dict with a few params based on input date-time object
    '''
    ret_val = {
        'hour'    : int(time.strftime('%I', tm).strip('0')),
        'minute'  : int(time.strftime('%M', tm)), 
        'is_am'   : time.strftime('%p', tm) == 'AM'
    }
    return ret_val


def get_day_info(dt=get_local_date()):
    ''' gets a dict with a few params based on input date-time object
    '''
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


def set_date(dt=datetime.date.today(), month=None, day=None, year=None):
    ''' return a datetime object, setting new month & day ranges
    '''
    ret_val = dt
    try:
        if not year : year  = dt.year
        if not month: month = dt.month
        if not day  : day   = dt.day
        ret_val = dt.replace(year, month, day)
    except:
        pass
    return ret_val


def pretty_date(dt=datetime.date.today(), fmt='%A, %B %d, %Y'):
    return dt.strftime(fmt)


def get_svc_date_tabs(dt, uri, more_tab=True, fmt='%m/%d/%Y', smfmt='%m/%d', pttyfmt='%A, %B %d, %Y'):
    ''' return 3 date strings representing the next WEEKDAY, SAT, SUN 
    '''
    ret_val = []

    #TODO: how to localize these here in python????
    #today=_$(u'Today')
    #more=_$(u'more')
    today='Today'
    more='more'

    # step 1: is 'today' the active tab, or is target date in future, so that's active, and we have a 'today' tab to left
    if datetime.date.today() == dt:
        ret_val.append({"name":today})
    else:
        ret_val.append({"name":today, "url": uri + "&date=" + datetime.date.today().strftime(fmt)})
        ret_val.append({"name":dt.strftime(smfmt).lstrip('0').replace('/0','/')})

    # step 2: figure out how many days from target is next sat, sunday and/or monday (next two service days different from today)
    delta1 = 1
    delta2 = 2
    if dt.weekday() < 5:
        # date is a m-f, so we're looking for next sat (delta1) and sun (delta 2)
        delta1 = 5 - dt.weekday()
        delta2 = delta1 + 1
    elif dt.weekday() == 6:
        # date is a sunday, so we're looking for monday (delta1), which is = 1 day off, and next sat (delta2) which is +6 days off 
        delta2 = 6

    d1 = dt + datetime.timedelta(days=delta1)
    d2 = dt + datetime.timedelta(days=delta2)
    #print "{0} {1} {2}={3} {4}={5}".format(dt, dt.weekday(), delta1, d1, delta2, d2)

    # step 3: add the next to service day tabs to our return array
    ret_val.append({"name":d1.strftime(smfmt).lstrip('0').replace('/0','/'), "url": uri + "&date=" + d1.strftime(fmt)})
    ret_val.append({"name":d2.strftime(smfmt).lstrip('0').replace('/0','/'), "url": uri + "&date=" + d2.strftime(fmt)})

    # TODO put the ret_val appen stuff in a separte method that builds up the dict...
    #      and add a pretty_date to that dict, so that we can create a css TOOLTIP that shows what weekday / date the 2/1, 2/5, 2/6 dates represent...
    #, "pretty_date": pretty_date(d1, pttyfmt)})

    # step 4: if we are not showing the date form, give the 'more' option which will show that form 
    if more_tab:
        ret_val.append({"name":more,   "url": uri + "&more&date=" + dt.strftime(fmt)})

    return ret_val

