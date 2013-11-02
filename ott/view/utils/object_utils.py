

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
