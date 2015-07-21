import logging
log = logging.getLogger(__file__)

import StringIO
import re

from pyramid.request import Request
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from pyramid.events import NewRequest
from pyramid.events import ApplicationCreated
from pyramid.events import subscriber

from ott.view.model.model import Model
from ott.view.model.mock import Mock

from ott.view.utils import schedule_tabs
from ott.view.utils import geocode_utils

from ott.utils.img.spark import sparkline_smooth
from ott.utils.img.qr import qr_to_stream
from ott.utils import html_utils
from ott.utils import object_utils
from ott.utils import transit_utils
from ott.utils import date_utils
from ott.utils.parse import TripParamParser

from ott.view.model.place import Place


def do_view_config(config):
    ''' adds the views (see below) and static directories to pyramid's config
    '''

    # routes setup
    config.add_route('index_desktop',                           '/')
    config.add_route('index_mobile',                            '/m')
    config.add_route('index_ws',                                '/ws')
    config.add_route('sparkline_desktop',                       '/sparkline')
    config.add_route('sparkline_mobile',                        '/m/sparkline')
    config.add_route('sparkline_ws',                            '/ws/sparkline')
    config.add_route('qrcode_desktop',                          '/qrcode')
    config.add_route('qrcode_mobile',                           '/m/qrcode')
    config.add_route('qrcode_ws',                               '/ws/qrcode')
    config.add_route('adverts_desktop',                         '/adverts.html')
    config.add_route('adverts_mobile',                          '/m/adverts.html')
    config.add_route('adverts_ws',                              '/ws/adverts.html')

    ###
    ### DESKTOP PAGES
    ###
    config.add_route('exception_desktop',                       '/exception.html')
    config.add_route('feedback_desktop',                        '/feedback.html')

    config.add_route('pform_standalone',                        '/pform_standalone.html')
    config.add_route('pform_no_includes',                       '/pform_no_includes.html')
    config.add_route('pform_example',                           '/pform_example.html')
    config.add_route('planner_form_desktop',                    '/planner_form.html')
    config.add_route('planner_geocode_desktop',                 '/planner_geocode.html')
    config.add_route('planner_desktop',                         '/planner.html')
    config.add_route('planner_walk_desktop',                    '/planner_walk.html')

    config.add_route('stop_select_form_desktop',                '/stop_select_form.html')
    config.add_route('stop_select_list_desktop',                '/stop_select_list.html')
    config.add_route('stop_select_geocode_desktop',             '/stop_select_geocode.html')

    config.add_route('stop_desktop',                            '/stop.html')
    config.add_route('stops_near_desktop',                      '/stops_near.html')
    config.add_route('stop_schedule_desktop',                   '/stop_schedule.html')

    config.add_route('map_place_desktop',                       '/map_place.html')

    ###
    ### MOBILE PAGES
    ###
    config.add_route('exception_mobile',                        '/m/exception.html')
    config.add_route('feedback_mobile',                         '/m/feedback.html')

    config.add_route('planner_form_mobile',                     '/m/planner_form.html')
    config.add_route('planner_geocode_mobile',                  '/m/planner_geocode.html')
    config.add_route('planner_mobile',                          '/m/planner.html')
    config.add_route('planner_walk_mobile',                     '/m/planner_walk.html')

    config.add_route('stop_select_form_mobile',                 '/m/stop_select_form.html')
    config.add_route('stop_select_form_mobile_short',           '/m/ss.html')
    config.add_route('stop_select_list_mobile',                 '/m/stop_select_list.html')
    config.add_route('stop_select_geocode_mobile',              '/m/stop_select_geocode.html')

    config.add_route('stop_mobile',                             '/m/stop.html')
    config.add_route('stop_mobile_short',                       '/m/s.html')
    config.add_route('stops_near_mobile',                       '/m/stops_near.html')
    config.add_route('stop_schedule_mobile',                    '/m/stop_schedule.html')

    config.add_route('map_place_mobile',                        '/m/map_place.html')

    ###
    ### WS PAGES
    ###
    config.add_route('exception_ws',                        '/ws/exception.html')
    config.add_route('feedback_ws',                         '/ws/feedback.html')

    config.add_route('planner_form_ws',                     '/ws/planner_form.html')
    config.add_route('planner_geocode_ws',                  '/ws/planner_geocode.html')
    config.add_route('planner_ws',                          '/ws/planner.html')
    config.add_route('planner_walk_ws',                     '/ws/planner_walk.html')

    config.add_route('stop_select_form_ws',                 '/ws/stop_select_form.html')
    config.add_route('stop_select_list_ws',                 '/ws/stop_select_list.html')
    config.add_route('stop_select_geocode_ws',              '/ws/stop_select_geocode.html')

    config.add_route('stop_ws',                             '/ws/stop.html')
    config.add_route('stops_near_ws',                       '/ws/stops_near.html')
    config.add_route('stop_schedule_ws',                    '/ws/stop_schedule.html')

    config.add_route('map_place_ws',                        '/ws/map_place.html')


@view_config(route_name='exception_mobile',  renderer='mobile/exception.html')
@view_config(route_name='exception_desktop', renderer='desktop/exception.html')
@view_config(route_name='exception_ws',      renderer='ws/exception.html')
def handle_exception(request):
    ret_val = {}
    return ret_val

@view_config(route_name='feedback_mobile',  renderer='mobile/feedback.html')
@view_config(route_name='feedback_desktop', renderer='desktop/feedback.html')
@view_config(route_name='feedback_ws',      renderer='ws/feedback.html')
def feedback(request):
    ret_val = {}
    ret_val['stop'] = None
    return ret_val

@view_config(route_name='planner_form_mobile',  renderer='mobile/planner_form.html')
@view_config(route_name='planner_form_desktop', renderer='desktop/planner_form.html')
@view_config(route_name='planner_form_ws',      renderer='ws/planner_form.html')
@view_config(route_name='pform_example',     renderer='shared/app/pform_example.html')
@view_config(route_name='pform_standalone',  renderer='shared/app/pform_standalone.html')
@view_config(route_name='pform_no_includes', renderer='shared/app/pform_no_includes.html')
def planner_form(request):
    ret_val = {}
    params = html_utils.planner_form_params(request)
    ret_val['params'] = params
    return ret_val

@view_config(route_name='planner_geocode_mobile',  renderer='mobile/planner_geocode.html')
@view_config(route_name='planner_geocode_desktop', renderer='desktop/planner_geocode.html')
@view_config(route_name='planner_geocode_ws',      renderer='ws/planner_geocode.html')
def planner_geocode(request):
    ''' for the ambiguous geocode page
    '''
    try:
        geo_place = None
        geo_type = html_utils.get_first_param(request, 'geo_type', 'place')
        if 'from' in geo_type:
            geo_place = html_utils.get_first_param(request, 'from')
        elif 'to' in geo_type:
            geo_place = html_utils.get_first_param(request, 'to')

        ret_val = geocode_utils.call_geocoder(request, geo_place, geo_type)
        adverts = request.model.get_adverts(request,  **request.params)
        ret_val['adverts'] = adverts
    except Exception, e:
        log.warning('{0} exception:{1}'.format(request.path, e))
        ret_val = make_subrequest(request, '/exception.html')
    return ret_val

@view_config(route_name='planner_mobile',  renderer='mobile/planner.html')
@view_config(route_name='planner_desktop', renderer='desktop/planner.html')
@view_config(route_name='planner_ws',      renderer='ws/planner.html')
def planner(request):
    ''' will either call the trip planner, or if we're missing params, redirect to the ambiguous geocode page
        basically, call the geocode checker, and then either call the ambiguous geocoder page, or plan the trip planner
    '''
    try:
        #import pdb; pdb.set_trace()
        ret_val = {}
        gc = geocode_utils.do_from_to_geocode_check(request)
        if gc['geocode_param']:
            ret_val = make_subrequest(request, '/planner_geocode.html', gc['query_string'], gc['geocode_param'])
        else:
            mapit = html_utils.get_first_param(request, 'mapit')
            if mapit:
                params = TripParamParser(request)
                params.set_from(gc['from']) 
                params.set_to(gc['to']) 
                map_params = params.map_url_params()
                ret_val = forward_request(request, 'http://ride.trimet.org?submit&' + map_params)
            else:
                ret_val = request.model.get_plan(gc['query_string'], **request.params)
                ret_val['cache'] = gc['cache']
                if ret_val and 'error' in ret_val:
                    msg = object_utils.get_error_message(ret_val)
                    ret_val = make_subrequest(request, '/exception.html', 'error_message={0}'.format(msg))
    except Exception, e:
        log.warning('{0} exception:{1}'.format(request.path, e))
        ret_val = make_subrequest(request, '/exception.html')

    return ret_val


@view_config(route_name='planner_walk_mobile',  renderer='mobile/planner_walk.html')
@view_config(route_name='planner_walk_desktop', renderer='desktop/planner_walk.html')
@view_config(route_name='planner_walk_ws',      renderer='ws/planner_walk.html')
def planner_walk(request):
    ret_val = None
    try:
        ret_val = request.model.get_plan(request.query_string, **request.params)
    except:
        ret_val = make_subrequest(request, '/exception.html')
    return ret_val


@view_config(route_name='stop_mobile_short', renderer='mobile/stop.html')
@view_config(route_name='stop_mobile',       renderer='mobile/stop.html')
@view_config(route_name='stop_desktop',      renderer='desktop/stop.html')
@view_config(route_name='stop_ws',           renderer='ws/stop.html')
def stop(request):
    stop = None
    has_coord = html_utils.get_first_param_is_a_coord(request, 'placeCoord')

    try:
        stop = request.model.get_stop(request.query_string, **request.params)
    except Exception, e:
        log.warning('{0} exception:{1}'.format(request.path, e))

    if stop and stop['has_errors'] is not True:
        ret_val = {}
        ret_val['stop'] = stop
    elif has_coord:
        coord = html_utils.get_first_param(request, 'placeCoord')
        ret_val = make_subrequest(request, '/stops_near.html', 'placeCoord={0}'.format(coord))
    else:
        ret_val = make_subrequest(request, '/exception.html', 'app_name=Stop Details page')
    return ret_val


@view_config(route_name='stop_schedule_mobile',  renderer='mobile/stop_schedule.html')
@view_config(route_name='stop_schedule_desktop', renderer='desktop/stop_schedule.html')
@view_config(route_name='stop_schedule_ws',      renderer='ws/stop_schedule.html')
def stop_schedule(request):
    html_tabs = stop_sched = alerts = None
    stop_id = html_utils.get_first_param(request, 'stop_id')
    route   = html_utils.get_first_param(request, 'route')
    try:
        url = 'stop_schedule.html?stop_id={0}&route={1}'.format(stop_id, route)
        html_tabs = schedule_tabs.get_tabs(request, url)
        stop_sched = request.model.get_stop_schedule(request.query_string, **request.params)
        alerts = transit_utils.get_stoptime_alerts(stop_sched)
    except Exception, e:
        log.warning('{0} exception:{1}'.format(request.path, e))

    if html_tabs and stop_sched and stop_sched['has_errors'] is not True:
        ret_val = {}
        ret_val['html_tabs'] = html_tabs
        ret_val['stop_sched'] = stop_sched
        ret_val['alerts'] = alerts
    else:
        ret_val = make_subrequest(request, '/exception.html', 'app_name=Stop Schedule page')
    return ret_val

@view_config(route_name='stop_select_form_mobile_short', renderer='mobile/stop_select_form.html')
@view_config(route_name='stop_select_form_mobile',       renderer='mobile/stop_select_form.html')
@view_config(route_name='stop_select_form_desktop',      renderer='desktop/stop_select_form.html')
@view_config(route_name='stop_select_form_ws',           renderer='ws/stop_select_form.html')
def stop_select_form(request):
    routes = None
    try:
        routes = request.model.get_routes(request.query_string, **request.params)
    except Exception, e:
        log.warning('{0} exception:{1}'.format(request.path, e))

    if routes and routes['has_errors'] is not True:
        ret_val = {}
        ret_val['place']  = html_utils.get_first_param(request, 'place')
        ret_val['routes'] = routes
    else:
        ret_val = make_subrequest(request, '/exception.html', 'app_name=Stop Select page')
    return ret_val

@view_config(route_name='stop_select_list_mobile',  renderer='mobile/stop_select_list.html')
@view_config(route_name='stop_select_list_desktop', renderer='desktop/stop_select_list.html')
@view_config(route_name='stop_select_list_ws',      renderer='ws/stop_select_list.html')
def stop_select_list(request):
    route_stops = None
    try:
        route_stops = request.model.get_route_stops(request.query_string, **request.params)
    except Exception, e:
        log.warning('{0} exception:{1}'.format(request.path, e))

    if route_stops and route_stops['has_errors'] is not True:
        ret_val = {}
        route = html_utils.get_first_param(request, 'route')
        ret_val['route_stops'] = route_stops
    else:
        ret_val = make_subrequest(request, '/exception.html', 'app_name=Route Stops page')
    return ret_val


@view_config(route_name='stop_select_geocode_mobile',  renderer='mobile/stop_select_geocode.html')
@view_config(route_name='stop_select_geocode_desktop', renderer='desktop/stop_select_geocode.html')
@view_config(route_name='stop_select_geocode_ws',      renderer='ws/stop_select_geocode.html')
def stop_select_geocode(request):
    place = html_utils.get_first_param(request, 'place')
    ret_val = geocode_utils.call_geocoder(request, place)
    return ret_val


@view_config(route_name='stops_near_mobile',  renderer='mobile/stops_near.html')
@view_config(route_name='stops_near_desktop', renderer='desktop/stops_near.html')
@view_config(route_name='stops_near_ws',      renderer='ws/stops_near.html')
def stops_near(request):
    ''' this routine is called by the stop lookup form.  we branch to either call the
        nearest stop routine (based on lat,lon coordiantes), or call stop.html directly

        this routine feels overly complex ... part of the problem is that we might see
        the stop id passed in via a string (place param gotten by SOLR / ajax), or the 
        stop might come in the string name from a geocoder, etc...

        Note that a log of logic is broken into 4 sub methods of stops_near ... these routiens
        will use (and possibly set) both request and ret_val variables in the parent scope
    '''
    ret_val = {}

    def call_near_ws(geo=None):
        p = Place.make_from_request(request)
        p.update_values_via_dict(geo)
        params = p.to_url_params()
        ret_val['place']   = p.__dict__
        ret_val['params']  = params
        num = 5
        if html_utils.get_first_param(request, 'show_more', None):
            num = 30
        params = "num={0}&".format(num) + params
        ret_val['nearest'] = request.model.get_stops_near(params, **request.params)
        ret_val['cache'] = []

    def check_place_for_stopid(place):
        ''' return what looks like a stop id in a string
        '''
        stop = None
        if place and "Stop ID" in place:
            s = place.split("Stop ID")
            if s and len(s) >= 2:
                stop = s[1].strip()
                stop = re.sub('[\W+\s]+.*', '', stop)
        return stop

    def geo_has_stopid(geo):
        ''' look for a stop id in the geocoder result
        '''
        stop = None
        try:
            if 'stop_id' in geo and geo['stop_id']:
                stop = geo['stop_id']
            elif 'name' in geo:
                stop = check_place_for_stopid(geo['name'])
        except:
            pass
        return stop

    def add_string_to_querystr(qs, str):
        ret_val = ''
        sep = ''
        if str:
            ret_val = str
            sep = '&'
        if qs and len(qs) > 0:
            ret_val = "{0}{1}{2}".format(ret_val, sep, qs)
        return ret_val

    def make_qs_with_stop_id(stop_id, rec=None):
        query_string = ''
        if rec and 'lat' in rec and 'lon' in rec:
            query_string = add_string_to_querystr(query_string, "placeCoord={0},{1}".format(rec['lat'], rec['lon']))
        if stop_id:
            query_string = add_string_to_querystr(query_string, "stop_id={0}".format(stop_id))
        if request.query_string:
            query_string = add_string_to_querystr(request.query_string, query_string)
        return query_string

    #import pdb; pdb.set_trace()

    # step 1: query has stop_id param ... call stop.html
    stop_id = html_utils.get_first_param_as_str(request, 'stop_id')
    if stop_id:
        ret_val = make_subrequest(request, '/stop.html', request.query_string)
    else:
        # step 2: place param has name with stop_id in it ... call stop.html
        place = html_utils.get_first_param_as_str(request, 'place')
        stop_id = check_place_for_stopid(place)
        if stop_id:
            qs = make_qs_with_stop_id(stop_id)
            ret_val = make_subrequest(request, '/stop.html', qs)
        else:
            # step 3: params have geocode information, call nearest with that information
            if geocode_utils.has_valid_geocode(request):
                call_near_ws()
            else:
                # step 4: geocode the place param and if we get a direct hit, call either stop or nearest
                geo = geocode_utils.call_geocoder(request, place)
                if geo and geo['count'] == 1:
                    single_geo = geo['geocoder_results'][0]
                    # step 4a: looking for stop id in geo result ... if there we'll call stop.html directly
                    stop_id = geo_has_stopid(single_geo)
                    if stop_id:
                        qs = make_qs_with_stop_id(stop_id, single_geo)
                        ret_val = make_subrequest(request, '/stop.html', qs)
                        # NOTE can't add 'cache' here, since this is a subrequest http call...

                    # step 4b: we're going to call nearest based on the geocode coordinates 
                    else:
                        call_near_ws(single_geo)
                        ret_val['cache'].append(geocode_utils.make_autocomplete_cache(place, single_geo))
                else:
                    ret_val = make_subrequest(request, '/stop_select_geocode.html')

    return ret_val


@view_config(route_name='map_place_mobile',  renderer='mobile/map_place.html')
@view_config(route_name='map_place_desktop', renderer='desktop/map_place.html')
@view_config(route_name='map_place_ws',      renderer='ws/map_place.html')
def map_place(request):
    ret_val = {}
    p = Place.make_from_request(request)
    ret_val['place'] = p.__dict__
    return ret_val


@view_config(route_name='sparkline_desktop')
@view_config(route_name='sparkline_mobile')
@view_config(route_name='sparkline_ws')
def sparkline(request):
    ''' returns a sparkline image in png format...
    '''
    response = Response(content_type='image/png')
    points = html_utils.get_param_as_list(request, 'points', float)
    im = sparkline_smooth(results=points) #, bg_color='#FF0000', fill_color='#0000FF'
    img_io = StringIO.StringIO()
    im.save(img_io, "PNG")
    img_io.seek(0)
    response.app_iter = img_io
    return response


@view_config(route_name='qrcode_desktop')
@view_config(route_name='qrcode_mobile')
@view_config(route_name='qrcode_ws')
def qrcode(request):
    ''' streams a qrcode image for the param 'content' (defaults to http://trimet.org)
    '''
    response = Response(content_type='image/png')
    content = html_utils.get_first_param(request, 'content', 'http://trimet.org')
    img_io = qr_to_stream(content)
    response.app_iter = img_io
    return response


@view_config(route_name='adverts_desktop', renderer='adverts.html')
@view_config(route_name='adverts_mobile',  renderer='adverts.html')
@view_config(route_name='adverts_ws',      renderer='adverts.html')
def adverts(request):
    ret_val = {}
    ret_val['bus_adverts']     = request.model.get_adverts("mode=bus&_LOCALE_=en",  **request.params)
    ret_val['bus_adverts_es']  = request.model.get_adverts("mode=bus&_LOCALE_=es",  **request.params)
    ret_val['rail_adverts']    = request.model.get_adverts("mode=rail&_LOCALE_=en", **request.params)
    ret_val['rail_adverts_es'] = request.model.get_adverts("mode=rail&_LOCALE_=es", **request.params)
    return ret_val


@view_config(route_name='index_desktop', renderer='index.html')
@view_config(route_name='index_mobile',  renderer='index.html')
@view_config(route_name='index_ws',      renderer='index.html')
def index_view(request):
    return {}


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    '''
       what do i do?

       1. I'm called at startup of the Pyramid app.  
       2. I could be used to make db connection (pools), etc...
    '''
    log.info('Starting pyramid server...')


@subscriber(NewRequest)
def new_request_subscriber(event):
    '''
       what do i do?

       1. entry point for a new server request
       2. configure the request context object (can insert new things like db connections or authorization to pass around in this given request context)
    '''
    log.debug("new request called -- request is 'started'")
    request = event.request
    request.model = get_model(request)
    settings = request.registry.settings
    request.add_finished_callback(cleanup)

@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    '''
        render the notfound.mako page anytime a request comes in that 
        the app does't have mapped to a page or method
    '''
    return {}


##
## view utils
##

def cleanup(request):
    '''
       what do i do?

       1. I was configured via the new_request_subscriber(event) method
       2. I'm called via a server event (when a request is 'finished')
       3. I could do random cleanup tasks like close database connections, etc... 
    '''
    log.debug("cleanup called -- request is 'finished'")


def is_mobile(request):
    return '/m/' in request.path_url

def is_ws(request):
    return '/ws/' in request.path_url


def get_path(request, path):
    ret_val = path
    if is_mobile(request):
        ret_val = '/m' + path
    if is_ws(request):
        ret_val = '/ws' + path
    return ret_val


def forward_request(request, path, query_string=None, extra_params=None):
    # http://ride.trimet.org?mapit=I&submit&${plan['params']['map_planner']}
    # def map_url_params(self, fmt="from={frm}&to={to}&time={time}&maxHours={max_hours}&date={month}/{day}/{year}&mode={mode}&optimize={optimize}&maxWalkDistance={walk_meters:.0f}&arriveBy={arrive_depart}"):
    return HTTPFound(location=path)

def make_subrequest(request, path, query_string=None, extra_params=None):
    ''' create a subrequest to call another page in the app...
        http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/subrequest.html
    '''
    # step 1: make a new request object...
    path = get_path(request, path)
    subreq = Request.blank(path)

    # step 2: default to request's querystring as default qs
    if query_string is None:
        query_string = request.query_string

     # step 3: pre-pend any extra stuff to our querytring
    if extra_params:
        newqs = extra_params
        if len(query_string) > 0:
            newqs = newqs + "&" + query_string
        query_string = newqs

    # step 4: finish the qs crap, and call this sucker...
    subreq.query_string = query_string
    ret_val = request.invoke_subrequest(subreq)
    return ret_val


MODEL_GLOBAL = None
def get_model(request):
    ''' @see make_views() below, which should have a model passed in to configure the model global 
    '''
    global MODEL_GLOBAL
    if MODEL_GLOBAL is None:
        # TODO ... this right?
        # TODO ... better way to attach this to view?
        # TODO ... multi-threading/
        # do something to create a model...
        url = html_utils.get_ini_param(request, 'ott.controller')
        MODEL_GLOBAL = Model(url)
    return MODEL_GLOBAL

