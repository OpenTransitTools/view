import logging
log = logging.getLogger(__file__)

from ott.view.utils import object_utils

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


def plan_title(title, frm, sep, to, fmt=u"{0} - {1} {2} {3}", def_val=''):
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


def plan_description(plan, title, arr, opt, using_txt, max_walk_txt, fmt=u"{0}<br/>{1} {2}, {3}<br/>{4} {5} <br/>{6}<br/>{7} {8}"):
    ''' used for getting a planner description in text
        mostly done here to encode strings for utf-8 carap
    '''
    ret_val = ''

    tm = dt = mode = walk = ''
    try:
        itinerary = get_itinerary(plan)
        tm = get_time(itinerary, plan['params']['is_arrive_by'])
        dt = itinerary['date_info']['pretty_date']

        mode  = plan['params']['modes']
        walk  = plan['params']['walk']

        using_txt = using_txt
        max_walk_txt = max_walk_txt
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

