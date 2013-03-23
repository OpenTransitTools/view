import logging
log = logging.getLogger(__file__)

import datetime
import time
from calendar import monthrange

def is_valid_route(route):
    ''' will further parse the route string, and check for route in GTFSdb
    '''
    ret_val = False
    if route is not None and len(route) > 0 and route != "None":
        # TODO: add route validity checking here ... 
        #       we might also allow for TriMet::19 v CTran::19 as a parameter
        #       default to first agency if no ::
        ret_val = True
    return ret_val


def get_time_info(t=time.localtime()):
    ''' gets a dict with a few params based on input date-time object
    '''
    # import pdb; pdb.set_trace()
    ret_val = {
        'hour'    : int(time.strftime('%I', t).strip('0')),
        'minute'  : int(time.strftime('%M', t)),
        'is_am'   : time.strftime('%p', t) == 'AM'
    }
    return ret_val

def get_day_info(dt=datetime.date.today()):
    ''' gets a dict with a few params based on input date-time object
    '''
    st,end=monthrange(dt.year, dt.month)
    ret_val = {
        'year'    : dt.year,
        'month'   : dt.month,
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


def get_param_as_list(request, name, prim=str):
    ''' utility function to parse a request object for a certain value (and return an integer based on the param if it's an int)
    '''
    ret_val = []
    try:
        p = get_first_param(request, name)  # get param
        l = p.split(',')                    # split the list on commas
        ret_val = map(prim, l)              # cast the values to a certain built-in (or 'primitive' in java) type
    except:
        log.warn('uh oh...')

    return ret_val

def get_first_param_as_int(request, name, def_val=None):
    ''' utility function to parse a request object for a certain value (and return an integer based on the param if it's an int)
    '''
    ret_val=get_first_param(request, name, def_val)
    try:
        ret_val = int(ret_val)
    except:
        pass
    return ret_val


def get_first_param_as_date(request, name='date', fmt='%m/%d/%Y', def_val=datetime.date.today()):
    ''' utility function to parse a request object for something that looks like a date object...
    '''
    ret_val = def_val
    try:
        dstr = get_first_param(request, name)
        if dstr is not None:
            ret_val = datetime.datetime.strptime(dstr, fmt).date()
    except:
        pass
    return ret_val


def get_first_param(request, name, def_val=None):
    '''
        utility function

        @return the first value of the named http param (remember, http can have multiple values for the same param name), 
        or def_val if that param was not sent via HTTP
    '''
    ret_val=def_val
    try:
        ret_val = request.params.getone(name)
    except:
        pass
    return ret_val


def unescape_html(dict_list):
    ''' replace html escaped &lt; and &gt; characters with < or >
        @see: http://stackoverflow.com/questions/1076536/replacing-values-in-a-python-list-dictionary
    '''
    for datadict in dict_list:
        for key, value in datadict.items():
            m = value.replace("&lt;", "<").replace("&gt;", ">")
            datadict[key] = m

