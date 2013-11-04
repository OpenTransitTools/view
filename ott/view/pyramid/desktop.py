import logging
log = logging.getLogger(__file__)

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from ott.view.locale.subscribers import get_translator  #_  = get_translator(request)
from ott.view.utils import html_utils
from ott.view.utils import object_utils
from ott.view.model.place import Place

@view_config(route_name='exception_desktop', renderer='desktop/exception.html')
def exception_desktop(request):
    ret_val = {}
    return ret_val

@view_config(route_name='feedback_desktop', renderer='desktop/feedback.html')
def feedback(request):
    ret_val = {}
    ret_val['stop'] = None
    return ret_val

@view_config(route_name='planner_form_desktop', renderer='desktop/planner_form.html')
def planner_form(request):
    ret_val = {}
    #import pdb; pdb.set_trace()
    params = html_utils.planner_form_params(request)
    ret_val['params'] = params
    return ret_val

def call_geocoder(request, no_geocode_msg='Undefined'):
    ret_val = {}

    geocode = html_utils.get_first_param(request, 'place')
    if geocode:
        res = request.model.get_geocode(geocode)
        if res and 'results' in res:
            ret_val['geocoder_results'] = res['results']
    else:
        _  = get_translator(request)
        geocode = _(no_geocode_msg)

    ret_val['place'] = geocode
    return ret_val


@view_config(route_name='planner_geocode_desktop', renderer='desktop/planner_geocode.html')
def planner_geocode(request):
    ret_val = call_geocoder(request)
    return ret_val


@view_config(route_name='planner_desktop', renderer='desktop/planner.html')
def planner(request):
    ret_val = None
    try:
        ret_val = request.model.get_plan(request.query_string, **request.params)
    except:
        # http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/subrequest.html
        subreq = Request.blank('/exception.html')
        subreq.query_string = request.query_string
        ret_val = request.invoke_subrequest(subreq)
    return ret_val

@view_config(route_name='planner_walk_desktop', renderer='desktop/planner_walk.html')
def planner_walk(request):
    ret_val = None
    try:
        ret_val = request.model.get_plan(request.query_string, **request.params)
    except:
        subreq = Request.blank('/exception.html')
        subreq.query_string = request.query_string
        ret_val = request.invoke_subrequest(subreq)
    return ret_val


@view_config(route_name='stop_desktop', renderer='desktop/stop.html')
def stop(request):
    stop   = request.model.get_stop(request.query_string, **request.params)
    ret_val = {}
    ret_val['stop'] = stop
    return ret_val

@view_config(route_name='stop_schedule_desktop', renderer='desktop/stop_schedule.html')
def stop_schedule(request):
    stop_id = html_utils.get_first_param(request, 'stop_id')
    route   = html_utils.get_first_param(request, 'route')
    url = 'stop_schedule.html?stop_id={0}&route={1}'.format(stop_id, route)

    ret_val = html_utils.service_tabs(request, url)
    ret_val['stop'] = request.model.get_stop_schedule(request.query_string, **request.params)
    return ret_val

@view_config(route_name='stop_select_form_desktop', renderer='desktop/stop_select_form.html')
def stop_select_form(request):
    ret_val = {}
    ret_val['place']  = html_utils.get_first_param(request, 'place')
    ret_val['routes'] = request.model.get_routes(request.query_string, **request.params)
    return ret_val

@view_config(route_name='stop_select_list_desktop', renderer='desktop/stop_select_list.html')
def stop_select_list(request):
    ret_val = {}
    route = html_utils.get_first_param(request, 'route')
    ret_val['route_stops'] = request.model.get_route_stops(request.query_string, **request.params)
    return ret_val

@view_config(route_name='stop_select_geocode_desktop', renderer='desktop/stop_select_geocode.html')
def stop_select_geocode(request):
    ret_val = call_geocoder(request)
    return ret_val

@view_config(route_name='stop_select_nearest_desktop', renderer='desktop/stop_select_nearest.html')
def stop_select_nearest(request):
    ret_val = {}
    p = Place.make_from_request(request)
    ret_val['place'] = p.__dict__
    return ret_val

@view_config(route_name='map_place_desktop', renderer='desktop/map_place.html')
def map_place(request):
    ret_val = {}
    p = Place.make_from_request(request)
    ret_val['place'] = p.__dict__
    return ret_val

