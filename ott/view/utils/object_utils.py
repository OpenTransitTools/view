'''
'''
import datetime
import simplejson as json
import logging
log = logging.getLogger(__file__)

def get_error_message(err, def_val=None):
    ''' return error message from an OTP error object
        {'error': {'msg': 'Origin is within a trivial distance of the destination.', 'id': 409}}
    '''
    ret_val = def_val
    try:
        ret_val = err.error.msg
    except:
        ret_val = def_val
    return ret_val

def update_object(tgt, src):
    ''' copy values from src to tgt, for any shared element names between the two objects
    '''
    for k, v in src.__dict__.items():
        try:
            if tgt.__dict__.has_key(k):
                tgt.__dict__[k] = v
        except:
            pass


def fix_url(url):
    ''' do things like escape the & in intersection names, ala "17th %26 Center"
    '''
    ret_val = url
    ret_val = ret_val.replace(" & ", " %26 ")
    return ret_val


def str_to_date(str_date, fmt_list=['%Y-%m-%d', '%m/%d/%Y'], def_val=None):
    ''' utility function to parse a request object for something that looks like a date object...
    '''
    if def_val is None:
        def_val = datetime.date.today()

    ret_val = def_val
    for fmt in fmt_list:
        try:
            d = datetime.datetime.strptime(str_date, fmt).date()
            if d is not None:
                ret_val = d
                break
        except Exception, e:
            log.warn(e)
    return ret_val


def pretty_date(dt, fmt="%A, %B %d, %Y", def_val=None):
    ret_val = def_val
    try:
        ret_val =  dt.strftime(fmt).replace(' 0',' ')  # "Monday, March 4, 2013"
    except Exception, e:
        log.warn(e)
    return ret_val

def pretty_time(dt, fmt=" %I:%M%p", def_val=None):
    ret_val = def_val
    try:
        ret_val = dt.strftime(fmt).lower().replace(' 0','').strip()  # "3:40pm"
    except Exception, e:
        log.warn(e)
    return ret_val

def make_date_from_timestamp(num, def_val=None):
    ret_val = def_val
    try:
        ret_val = datetime.datetime.fromtimestamp(num)
    except Exception, e:
        log.warn(e)
    return ret_val

def is_date_between(start, end, now=None):
    ''' will compare a datetime (now) to a start and end datetime.
        the datetime being compared defaults to 'now()'
        if a date() submitted, then defaults will be added to turn that into a datetime() for date() at 12am
        if a time() is submitted, then defaults will be added to turn that into a datetime() of today at time()
    '''
    ret_val = False

    try:
        if now is None:
            now = datetime.datetime.now()
        elif type(now) is datetime.date:
            now = datetime.datetime.combine(now, datetime.datetime.min.time())
        elif type(now) is datetime.time:
            now = datetime.datetime.combine(datetime.date.today(), now)

        if type(start) is datetime.datetime and type(end) is datetime.datetime:
            if start < now < end:
                ret_val = True
        elif type(start) is datetime.datetime:
            if start < now:
                ret_val = True
        elif type(end) is datetime.datetime:
            if now < end:
                ret_val = True
    except Exception, e:
        log.warn(e)
    return ret_val


def military_to_english_time(time, fmt="{0}:{1}{2}"):
    ''' assumes 08:33:55 and 22:33:42 type times
        will return 8:33am and 10:33pm
        (not we floor the minutes)
    '''
    ret_val = time
    try:
        t = time.split(":")
        h = int(t[0])
        m = t[1]
        ampm = "am"
        if h >= 12:
            ampm = "pm"
        if h >= 24:
            ampm = "am"
        h = h % 12
        if h == 0:
            h = 12

        ret_val = fmt.format(h, m, ampm)
    except:
        pass

    return ret_val


def has_content(obj):
    ret_val = False
    if obj:
        ret_val = True
        if isinstance(obj, basestring) and len(obj) <= 0:
            ret_val = False
    return ret_val


def safe_str(obj, def_val=''):
    ret_val = def_val
    try:
        ret_val = str(obj)
    except:
        pass
    return ret_val

def safe_int(obj, def_val=None):
    ret_val = def_val
    try:
        ret_val = int(obj)
    except:
        pass
    return ret_val


def safe_dict_val(obj, key, def_val=None):
    ret_val = def_val
    try:
        ret_val = obj[key]
    except:
        pass
    return ret_val



def strip_tuple(obj, def_val=None):
    ret_val = def_val
    try:
        ret_val = obj[0]
    except:
        pass
    return ret_val

def strip_tuple_list(obj_list, def_val=None):
    ret_val = def_val
    try:
        rv = []
        for o in obj_list:
            z = strip_tuple(o)
            rv.append(z)
        ret_val = rv
    except:
        pass
    return ret_val


def to_str(s, def_val=''):
    ''' multi-byte compliant version of str() unicode conversion...
    '''
    ret_val = def_val
    try:
        ret_val = s.encode('utf-8')
    except:
        try:
            ret_val = str(s)
        except:
            pass
    return ret_val

def to_code(s, def_val=''):
    ''' multi-byte compliant version of str() unicode conversion...
    '''
    ret_val = def_val
    try:
        ret_val = s.decode('utf-8')
    except:
        try:
            ret_val = str(s)
        except:
            pass
    return ret_val

def to_str_code(s, def_val=''):
    ''' multi-byte compliant version of str() unicode conversion...
    '''
    ret_val = def_val
    try:
        ret_val = s.decode('utf-8')
    except:
        try:
            ret_val = str(s)
        except:
            pass
    return ret_val
