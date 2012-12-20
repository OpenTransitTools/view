
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
