
def to_int(val, def_val):
    ret_val = def_val
    try:
        ret_val = int(val)
    except:
        pass
    return ret_val

def ll_from_str(str, def_val=None, to_float=False):
    ''' break 45.5,-122.5 to lat,lon components
    '''
    lat = def_val
    lon = def_val
    try:
        ll  = str.split(',')
        lat = ll[0].strip()
        lon = ll[1].strip()
        if to_float:
            lat = float(lat)
            lon = float(lon)
    except:
        pass
    return lat,lon

