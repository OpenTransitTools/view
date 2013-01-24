import datetime
from calendar import monthrange

def get_day_info(dt=datetime.date.today()):
    st,end=monthrange(dt.year, dt.month)
    ret_val = {
        'year'    : dt.year,
        'month'   : dt.month,
        'numdays' : end,
        'day'     : dt.day
    }
    return ret_val


def pretty_date(dt=datetime.date.today(), fmt='%A %B, %d, %Y'):
    return dt.strftime(fmt)


def get_svc_date_tabs(dt, uri, fmt='%m/%d/%Y', smfmt='%m/%d'):
    ''' return 3 date strings representing the next WEEKDAY, SAT, SUN 
    '''
    #TODO: how to localize these here in python????
    #today=_$(u'Today')
    #more=_$(u'more')
    today='Today'
    more='more'

    d1 = dt
    d2 = dt

    ret_val = [
        {"name":today},
        {"name":dt.strftime(smfmt), "url": uri + "&date=" + dt.strftime(fmt)},
        {"name":d1.strftime(smfmt), "url": uri + "&date=" + d1.strftime(fmt)},
        {"name":more,   "url": uri + "&more&date=" + d2.strftime(fmt)}
    ]
    return ret_val

def get_first_param_as_int(request, name, def_val=None):
    '''
        utility function
    '''
    ret_val=get_first_param(request, name, def_val)
    try:
        ret_val = int(ret_val)
    except:
        pass
    return ret_val


def get_first_param_as_date(request, name='date', fmt='%m/%d/%Y', def_val=datetime.date.today()):
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
