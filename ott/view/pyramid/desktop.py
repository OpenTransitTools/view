from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ott.view.utils import html_utils


class Place(object):
    def __init__(self, name=None, lat=None, lon=None, city=None):
        self.set_values(name, lat, lon, city)

    def set_values(self, name=None, lat=None, lon=None, city=None):
        self.name = name
        self.lat = lat 
        self.lon = lon
        self.city = city

    def set_values_via_place_str(self, place):
        ''' will set the values of a <name>::<lat>,<lon>::<city> string into a place object
            ala PDX::45.5,-122.5::Portland will populate the Place object attributes
        '''
        try:
            # import pdb; pdb.set_trace() 
            p = place.split("::")
            if p[0] and len(p[0]) > 0:
                self.name = p[0]
            if p[1] and len(p[1]) > 0 and ',' in p[1]:
                ll = p[1].split(',')
                if ll and len(ll) >= 2:
                    self.lat = ll[0].strip()
                    self.lon = ll[1].strip()
            if p[2] and len(p[2]) > 0:
                self.city = p[2]
        except:
            pass


    @classmethod
    def make_from_request(cls, request):
        ret_val = Place()
        try:
            name = html_utils.get_first_param(request, 'name')
            # TODO localize...
            if name is None: name = 'Undefined Location'
            lat  = html_utils.get_first_param(request, 'lat')
            lon  = html_utils.get_first_param(request, 'lon')
            city = html_utils.get_first_param(request, 'city')
            ret_val.set_values(name, lat, lon, city)

            place = html_utils.get_first_param(request, 'place')
            ret_val.set_values_via_place_str(place)
        except: pass
        return ret_val

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
    params = html_utils.planner_form_params(request)
    ret_val['params'] = params
    return ret_val


@view_config(route_name='planner_desktop', renderer='desktop/planner.html')
def planner(request):
    ret_val = None
    try:
        ret_val = request.model.get_plan(request.query_string, **request.params)
    except:
        url = "{0}{1}?{2}".format(request.application_url, '/exception.html', request.query_string)
        ret_val = HTTPFound(location=url, headers=request.headers)
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
    ret_val['routes'] = request.model.get_routes(request.query_string, **request.params)
    ret_val['place']  = {'name':'822 SE XXX Street', 'lat':'45.5', 'lon':'-122.5'}
    return ret_val

@view_config(route_name='stop_select_list_desktop', renderer='desktop/stop_select_list.html')
def stop_select_list(request):
    route = html_utils.get_first_param(request, 'route')
    ret_val = {}
    ret_val['route_stops'] = request.model.get_route_stops(request.query_string, **request.params)
    return ret_val

@view_config(route_name='stop_select_geocode_desktop', renderer='desktop/stop_select_geocode.html')
def stop_select_geocode(request):
    ret_val = {}
    ret_val['stop'] = request.model.get_stop(request.query_string, **request.params)
    return ret_val

@view_config(route_name='stop_select_geocode_nearest_desktop', renderer='desktop/stop_select_geocode_nearest.html')
def stop_select_geocode_nearest(request):
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


@view_config(route_name='nearest_service_form_desktop', renderer='desktop/nearest_service_form.html')
def nearest_service_form(request):
    ret_val = {}
    ret_val['routes'] = request.model.get_routes(request.query_string, **request.params)
    ret_val['place']  = {'name':'822 SE XXX Street', 'lat':'45.5', 'lon':'-122.5'}
    return ret_val

@view_config(route_name='nearest_service_geocode_desktop', renderer='desktop/nearest_service_geocode.html')
def nearest_service_geocode(request):
    ret_val = {}
    ret_val['stop'] = request.model.get_stop(request.query_string, **request.params)
    return ret_val

@view_config(route_name='nearest_service_desktop', renderer='desktop/nearest_service.html')
def nearest_service(request):
    ret_val = {}
    ret_val['routes'] = request.model.get_routes(request.query_string, **request.params)
    ret_val['place']  = {'name':'822 SE XXX Street', 'lat':'45.5', 'lon':'-122.5'}
    return ret_val


