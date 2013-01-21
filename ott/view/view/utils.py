

def get_svc_date_tabs(date, uri):
    ''' return 3 date strings representing the next WEEKDAY, SAT, SUN 
    '''
    #TODO: how to localize these here in python????
    #today=_$(u'Today')
    #more=_$(u'more')
    today='Today'
    more='more'

    if date is None:
        date = '1/19'

    ret_val = [
        {"name":today},
        {"name":"1/39", "url": uri + "&date=01/19/2013"},
        {"name":"1/20", "url": uri + "&date=01/20/2013"},
        {"name":more,   "url": uri + "&date=01/20/2013&more"}
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
