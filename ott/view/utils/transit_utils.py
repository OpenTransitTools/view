import logging
log = logging.getLogger(__file__)

from ott.view.utils import object_utils
from ott.view.utils.modes import Modes

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


def plan_title(title, frm, sep, to, fmt="{0} - {1} {2} {3}", def_val=''):
    ''' used for getting a planner title
        mostly done here to encode strings for utf-8 crap
    '''
    ret_val = def_val
    #import pdb; pdb.set_trace()
    try:
        ret_val = fmt.format(object_utils.to_str(title), object_utils.to_str(frm), object_utils.to_str(sep), object_utils.to_str(to))
    except Exception, e:
        log.debug(e)
        try:
            ret_val = object_utils.to_str(title)
        except:
            pass
        if not object_utils.has_content(ret_val):
            ret_val = def_val
    return ret_val


def plan_description(plan, title, arr, opt, using_txt, max_walk_txt, fmt="{0}<br/>{1} {2}, {3}<br/>{4} {5} <br/>{6}<br/>{7} {8}"):
    ''' used for getting a planner description in text
        mostly done here to encode strings for utf-8 carap
    '''
    ret_val = ''

    tm = dt = mode = walk = ''
    try:
        itinerary = get_itinerary(plan)
        tm = get_time(itinerary, plan['params']['is_arrive_by'])
        dt = itinerary['date_info']['pretty_date']

        mode  = object_utils.to_str(plan['params']['modes'])
        walk  = plan['params']['walk']

        using_txt = object_utils.to_str(using_txt)
        max_walk_txt = object_utils.to_str(max_walk_txt)
        title = object_utils.to_str(title)
        arr = object_utils.to_str(arr)
        opt = object_utils.to_str(opt)
        
    except Exception, e:
        log.debug(e)

    ret_val = fmt.format(title, arr, tm, dt, using_txt, mode, opt, max_walk_txt, walk)
    return ret_val


def get_time(itinerary, is_arrive_by):
    if is_arrive_by:
        time = itinerary['date_info']['end_time']
    else:
        time = itinerary['date_info']['start_time']
    return time

def get_itinerary(plan):
    ''' find target itinerary
    ''' 
    for itin in plan['itineraries']:
        itinerary = itin
        if itin['selected']:
            break
    return itinerary

def has_transit(itinerary):
    ''' see if there's a transit leg in our list...
    '''
    ret_val = False
    for leg in itinerary['legs']:
        if leg['mode'] in Modes.TRANSIT_MODES:
            ret_val = True
            break
    return ret_val

def fare(leg, itinerary):
    ''' TODO: figure out what to return here:

        if line 83 or 115 (for TriMet) are free to ride...
        if line TRAM then fare is $4.00 round trip...
        if ???  bunch of different fare rules...
    '''
    return True

def has_fare(itinerary):
    ''' tell whether this itinerary has a fare....
    '''
    ret_val = False
    for leg in itinerary['legs']:
        if leg['mode'] in Modes.TRANSIT_MODES:
            if fare(leg, itinerary):
                ret_val = True
                break
    return ret_val
