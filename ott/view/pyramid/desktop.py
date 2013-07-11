from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ott.view.utils import html_utils


@view_config(route_name='exception_desktop', renderer='desktop/exception.html')
def exception_desktop(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    return ret_val


@view_config(route_name='planner_form_desktop', renderer='desktop/planner_form.html')
def planner_form(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    params = html_utils.planner_form_params(request)
    ret_val['params']    = params

    return ret_val


@view_config(route_name='planner_itin_desktop', renderer='desktop/planner.html')
def planner_itin(request):
    '''
       what do i do?
       1. 
       2. ...
    '''
    ret_val = None
    try:
        ret_val = request.model.get_plan(request.query_string, **request.params)
    except:
        url = "{0}{1}?{2}".format(request.application_url, '/exception.html', request.query_string)
        ret_val = HTTPFound(location=url, headers=request.headers)
        print url

    return ret_val


@view_config(route_name='stop_desktop', renderer='desktop/stop.html')
def stop(request):
    '''
       what do i do?
       1. ...
    '''
    stop   = request.model.get_stop(request.query_string, **request.params)
    routes = request.model.get_routes(request.query_string, **request.params)
    if stop and routes:
        stop['routes'] = routes
        stop['alerts'] = request.model.get_alerts(routes, stop['id'])

    ret_val = {}
    ret_val['stop'] = stop

    return ret_val


@view_config(route_name='stop_schedule_desktop', renderer='desktop/stop_schedule.html')
def stop_schedule(request):
    '''
       what do i do?
       1. 
    '''
    ret_val = html_utils.service_tabs(request, 'stop_schedule.html?route={0}')
    ret_val['stop'] = request.model.get_stop_schedule(request.query_string, **request.params)

    return ret_val


@view_config(route_name='stop_geocode_desktop', renderer='desktop/stop_geocode.html')
def stop_geocode(request):
    '''
       what do i do?
       1. ...
    '''
    ret_val = {}
    ret_val['stop'] = request.model.get_stop(request.query_string, **request.params)

    return ret_val


@view_config(route_name='route_stop_desktop', renderer='desktop/route_stop_list.html')
def route_stops_list(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    route = html_utils.get_first_param(request, 'route')
    ret_val = {}
    ret_val['route_stops'] = request.model.get_route_stops(request.query_string, **request.params)

    return ret_val


@view_config(route_name='find_stop_desktop', renderer='desktop/find_stop.html')
def find_stop(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    ret_val['routes'] = request.model.get_routes()
    ret_val['place']  = {'name':'822 SE XXX Street', 'lat':'45.5', 'lon':'-122.5'}

    return ret_val


@view_config(route_name='feedback_desktop', renderer='desktop/feedback.html')
def feedback(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    stop = request.model.get_stop()
    stop['routes'] = request.model.get_routes()

    ret_val = {}
    ret_val['stop'] = stop

    return ret_val


@view_config(route_name='tracker_desktop', renderer='desktop/tracker.html')
def tracker(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    ret_val['routes'] = request.model.get_routes()['routes']

    return ret_val
