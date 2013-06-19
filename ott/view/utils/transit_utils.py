
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
