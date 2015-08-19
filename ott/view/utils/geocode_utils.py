import logging
log = logging.getLogger(__file__)

from ott.utils import html_utils
from ott.utils import geo_utils

##
## TODO: the routines below are used by the view project... 
##       they could be better placed / refactored into  ott.utils.parse 
##

def has_valid_geocode(request):
    # try 1: placeCoord parameter?
    coord = html_utils.get_first_param_is_a_coord(request, 'placeCoord')
    if coord:
        return True


    # try 2: place parameter?
    coord = html_utils.get_first_param_is_a_coord(request, 'place')
    if coord:
        return True

    # try 3: lat/lon parameters
    lat = html_utils.get_first_param(request, 'lat')
    lon = html_utils.get_first_param(request, 'lon')
    if lat and lon:
        return True

    # no valid geocode in request, so fail
    return False

def call_solr_geocoder(request, place):
    '''  call the geocoder service
    '''
    ret_val = None
    if place:
        res = request.model.get_geocode(place)
        if has_content(res, 'results'):
            ret_val = res['results']
    return ret_val

def call_atis_geocoder(request, place):
    '''  call the geocoder service
    '''
    ret_val = None
    if place:
        res = request.model.get_atis_geocode(place)
        if has_content(res, 'results'):
            ret_val = res['results']
    return ret_val

def call_geocoder(request, geo_place=None, geo_type='place', no_geocode_msg='Undefined'):
    ''' hybrid ATIS / SOLR geocoder
    '''
    ret_val = {
        "count" : 0,
        "geo_type" : geo_type,
        "geo_place" : geo_place,
        "geocoder_results" : None
    }

    #import pdb; pdb.set_trace()
    res = call_atis_geocoder(request, geo_place)
    if res and len(res) > 0:
        ret_val['count'] = len(res)
        ret_val['geocoder_results'] = res
    else:
        res = call_solr_geocoder(request, geo_place)
        if res and len(res) > 0:
            ret_val['count'] = len(res)
            ret_val['geocoder_results'] = res
        else:
            # when no results, we add the no geocode msg (e.g., 'Undefined') as the place name...
            ret_val['geo_place'] = no_geocode_msg

    return ret_val

def do_from_to_geocode_check(request):
    ''' checks whether we have proper coordinates for the from & to params
        if we're missing a coordinate, we'll geocode and see if there's a direct hit
        if no direct hit, we return the geocode_paaram that tells the ambiguous redirect page what to do...

        @return: a modified query string, and any extra params needed for the geocoder 
    '''
    ret_val = {'query_string':None, 'geocode_param':None, 'from':None, 'to':None, 'cache':[]}

    # step 1: check for from & to coord information in the url
    has_from_coord = geo_utils.is_param_a_coord(request, 'from')
    has_to_coord   = geo_utils.is_param_a_coord(request, 'to')
    qs = request.query_string

    # step 2: check we need to geocode the 'from' param ...
    if has_from_coord is False:
        ret_val['geocode_param'] = 'geo_type=from'

        # step 3a: does the 'from' param need geocoding help?  do we have a param to geocode?
        frm = html_utils.get_first_param(request, 'from')
        if frm and len(frm) > 0:

            # step 3b: we have something to geocode, so call the geocoder hoping to hit on a single result
            g = call_geocoder(request, frm, 'from')
            if g and g['count'] == 1:
                # step 3c: got our single result, so now add that to our query string...
                has_from_coord = True
                doc = g['geocoder_results'][0]
                fp = geo_utils.solr_to_named_param(doc, frm)
                qs = "from={0}&{1}".format(fp, qs)
                qs = qs.replace("&fromCoord=&", "&").replace("&fromCoord=None&", "&") # strip bogus stuff off...

                # step 3d: clear flag and set newly geocoded 'from' parameter
                ret_val['geocode_param'] = None
                ret_val['from'] = fp
                ret_val['cache'].append(make_autocomplete_cache(frm, doc))


    # step 4: check that we need to geocode the 'to' param 
    if has_to_coord is False and has_from_coord is True:
        ret_val['geocode_param'] = 'geo_type=to'

        # step 4a: does the 'to' param need geocoding help?  do we have a param to geocode?
        to = html_utils.get_first_param(request, 'to')
        if to and len(to) > 0:

            # step 4b: we have something to geocode, so call the geocoder hoping to hit on a single result
            g = call_geocoder(request, to, 'to')
            if g and g['count'] == 1:
                # step 4c: got our single result, so now add that to our query string...
                has_to_coord = True
                doc = g['geocoder_results'][0]
                tp = geo_utils.solr_to_named_param(doc, to)
                qs = "to={0}&{1}".format(tp, qs)
                qs = qs.replace("&toCoord=&", "&").replace("&toCoord=None&", "&") # strip bogus stuff off...

                # step 4d: clear flag and set newly geocoded 'to' parameter
                ret_val['geocode_param'] = None
                ret_val['to'] = tp
                ret_val['cache'].append(make_autocomplete_cache(to, doc))

    # step 5: assign query string to return
    ret_val['query_string'] = qs
    return ret_val

def make_place_from_stop_request(request, stop):
    place = html_utils.get_first_param(request, 'place')
    name = name_from_named_place(place, place)
    ret_val = geo_utils.make_place(name, lat, lon)

def has_content(geo, el='geocoder_results'):
    ret_val = False
    try:
        if geo and el in geo and geo[el][0] and len(geo[el][0]) > 0:
            ret_val = True
    except Exception, e:
        log.warning('exception:{0}'.format(e))
        ret_val = False
    return ret_val

def make_autocomplete_cache(frm, doc):
    ''' take a SOLR doc, and make an entry for the autocomplete cache
    '''
    ret_val = {'label':frm, 'lat':doc['lat'], 'lon':doc['lon']}
    return ret_val
