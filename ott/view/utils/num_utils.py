
def to_int(val, def_val):
    ret_val = def_val
    try:
        ret_val = int(val)
    except:
        pass
    return ret_val