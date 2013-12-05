import datetime
import logging
log = logging.getLogger(__file__)

import date_utils
import num_utils
import transit_utils

from ott.view.locale.subscribers import get_translator


def service_tabs(request, url):
    '''
    '''
    date  = get_first_param_as_date(request)
    month = get_first_param_as_int(request, 'month')
    day   = get_first_param_as_int(request, 'day')
    date  = date_utils.set_date(date, month, day)
    more  = get_first_param(request, 'more')

    ret_val = {}
    ret_val['more_form']   = date_utils.get_day_info(date)
    ret_val['pretty_date'] = date_utils.pretty_date(date)
    ret_val['tabs'] = date_utils.get_svc_date_tabs(date, url, more is None, get_translator(request)) 

    return ret_val


def planner_form_params(request):
    '''
    '''
    #import pdb; pdb.set_trace()

    # step 0: default values for the trip planner form 
    dt = date_utils.get_day_info()
    tm = date_utils.get_time_info()

    ret_val = {
        "fromPlace" : None,
        "fromCoord" : None,
        "toPlace"   : None,
        "toCoord"   : None,
        "Hour"      : tm['hour'],
        "Minute"    : tm['minute'],
        "AmPm"      : "am" if tm['is_am'] else "pm",
        "is_am"     : tm['is_am'],
        "month"     : dt['month'],
        "day"       : dt['day'],
        "year"      : dt['year'],
        "numdays"   : dt['numdays'],
        "Arr"       : False,
        "Walk"      : 840,
        "optimize"  : "QUICK",
        "mode"      : "TRANSIT,WALK"
    }

    # step 1: get params dict
    params = params_to_dict(request)

    # step 2: blanket assignment
    for k,v in params.items():
        #import pdb; pdb.set_trace()
        if k in ret_val and v is not None and len(v) > 0:
            if type(ret_val[k]) == bool:
                ret_val[k] = (v == 'True')
            if type(ret_val[k]) == int:
                ret_val[k] = num_utils.to_int(v, ret_val[k]) 
            else:
                ret_val[k] = v

    # step 3: handle from & to
    if "from" in params and len(params["from"]) > 0:
        parts = params["from"].split("::") 
        ret_val["fromPlace"] = parts[0]
        if len(parts) > 1:
            ret_val["fromCoord"] = parts[1]

    if "to" in params and len(params["to"]) > 0:
        parts = params["to"].split("::") 
        ret_val["toPlace"] = parts[0]
        if len(parts) > 1:
            ret_val["toCoord"] = parts[1]

    # step 4: special handle other params...
    ret_val["is_am"] = True if ret_val['AmPm'] == "am" else False
    ret_val["min"] = ret_val["optimize"]  # TODO remove me by changing min to optimize all over...

    return ret_val


def params_to_dict(request):
    ''' turn Pyramid's  MultDict of GET params to a normal dict.  
        multi-values will only use the first param value (and save off all to special _all param)
    '''
    ret_val = {}
    try:
        params = request.params.mixed()
        # loop through the params and assign them to the return variable
        for key, value in params.items():
            # only use the first value of a list (but save off other values to a _all variable
            if isinstance(value, (list, tuple)):
                ret_val[key] = value[0]
                ret_val[key + "_all"] = value
            else:
                ret_val[key] = value

        # save off the full query string into this dict too...
        #TODO: this is a good idea, bad implementation == makes the URL grow expo-large REALLY BAD 
        #if request.query_string and len(request.query_string) > 0:
        #    ret_val['query_string'] = request.query_string 
    except:
        # assume that request is the dict / string for params, and hope for the best...
        ret_val = request

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


def get_first_param_as_float(request, name, def_val=None):
    ''' utility function to parse a request object for a certain value (and return an integer based on the param if it's an int)
    '''
    ret_val=get_first_param(request, name, def_val)
    try:
        ret_val = float(ret_val)
    except:
        pass
    return ret_val

def get_first_param_is_a_coord(request, name, def_val=False):
    ''' looks for a string, which has a comma (assuming lat,lon) and is at least 7 chars in length ala 0.0,0.0
    '''
    ret_val = def_val
    try:
        val = get_first_param(request, name, def_val)
        if len(val) > 6 and ',' in val:
            ret_val = True
    except:
        pass
    return ret_val

def get_first_param_as_coord(request, name, def_val=None, to_float=False):
    ''' return lat,lon floats
    '''
    val = get_first_param(request, name, def_val)
    lat,lon = num_utils.ll_from_str(val, def_val, to_float)
    return lat,lon

def get_first_param_as_boolean(request, name, def_val=False):
    ''' utility function to get a variable
    '''
    ret_val = def_val

    val=get_first_param(request, name, def_val)
    try:
        if isinstance(val, bool):
            ret_val = val
        elif isinstance(val, str) or isinstance(val, unicode):
            if val.lower() == 'true':
                ret_val = True
            else: 
                ret_val = False
    except:
        pass
    return ret_val


def get_first_param_as_date(request, name='date', fmt='%m/%d/%Y', def_val=None):
    ''' utility function to parse a request object for something that looks like a date object...
    '''
    if def_val is None:
        def_val = datetime.date.today()

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
        l = request.params.getall(name)
        if l and len(l) > 0:
            ret_val = l[0]
    except:
        pass
    return ret_val

def get_lang(request, def_val="en"):
    return get_first_param(request, "_LOCALE_", def_val)


def unescape_html(dict_list):
    ''' replace html escaped &lt; and &gt; characters with < or >
        @see: http://stackoverflow.com/questions/1076536/replacing-values-in-a-python-list-dictionary
    '''
    for datadict in dict_list:
        for key, value in datadict.items():
            m = value.replace("&lt;", "<").replace("&gt;", ">")
            datadict[key] = m

