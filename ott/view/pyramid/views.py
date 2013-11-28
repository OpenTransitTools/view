import logging
log = logging.getLogger(__file__)

import StringIO

from pyramid.request import Request
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from pyramid.events import NewRequest
from pyramid.events import ApplicationCreated
from pyramid.events import subscriber

from ott.view.locale.subscribers import get_translator  #_  = get_translator(request)

from ott.view.model.model import Model
from ott.view.model.mock import Mock

from ott.view.utils.spark import sparkline_smooth
from ott.view.utils.qr import qr_to_stream
from ott.view.utils import html_utils
from ott.view.utils import object_utils
from ott.view.model.place import Place


def do_view_config(config):
    ''' adds the views (see below) and static directories to pyramid's config
        TODO: is there a better way to dot this (maybe via an .ini file)
    '''

    # routes setup
    config.add_route('index_desktop',                           '/')
    config.add_route('index_mobile',                            '/m')
    config.add_route('sparkline_desktop',                       '/sparkline')
    config.add_route('sparkline_mobile',                        '/m/sparkline')
    config.add_route('qrcode_desktop',                          '/qrcode')
    config.add_route('qrcode_mobile',                           '/m/qrcode')
    config.add_route('adverts_desktop',                         '/adverts.html')
    config.add_route('adverts_mobile',                          '/m/adverts.html')

    ###
    ### DESKTOP PAGES
    ###
    config.add_route('exception_desktop',                       '/exception.html')
    config.add_route('feedback_desktop',                        '/feedback.html')

    config.add_route('pform_standalone',                        '/pform_standalone.html')
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


@view_config(route_name='exception_mobile',  renderer='mobile/exception.html')
@view_config(route_name='exception_desktop', renderer='desktop/exception.html')
def handle_exception(request):
    ret_val = {}
    return ret_val

@view_config(route_name='feedback_mobile', renderer='mobile/feedback.html')
@view_config(route_name='feedback_desktop', renderer='desktop/feedback.html')
def feedback(request):
    ret_val = {}
    ret_val['stop'] = None
    return ret_val

@view_config(route_name='planner_form_mobile', renderer='mobile/planner_form.html')
@view_config(route_name='planner_form_desktop', renderer='desktop/planner_form.html')
@view_config(route_name='pform_example',    renderer='shared/app/pform_example.html')
@view_config(route_name='pform_standalone', renderer='shared/app/pform_standalone.html')
def planner_form(request):
    #import pdb; pdb.set_trace()
    ret_val = {}
    params = html_utils.planner_form_params(request)
    ret_val['params'] = params
    return ret_val


def call_geocoder(request, geo_place='', geo_type='place', no_geocode_msg='Undefined'):
    ret_val = {}

    count = 0
    if geo_place:
        res = request.model.get_geocode(geo_place)
        if res and 'results' in res:
            ret_val['geocoder_results'] = res['results']
            count = len(ret_val['geocoder_results'])
    else:
        _  = get_translator(request)
        geo_place = _(no_geocode_msg)

    ret_val['geo_type']  = geo_type
    ret_val['geo_place'] = geo_place
    ret_val['count'] = count
    return ret_val


@view_config(route_name='planner_geocode_mobile', renderer='mobile/planner_geocode.html')
@view_config(route_name='planner_geocode_desktop', renderer='desktop/planner_geocode.html')
def planner_geocode(request):
    geo_place = None
    geo_type = html_utils.get_first_param(request, 'geo_type', 'place')
    if 'from' in geo_type:
        geo_place = html_utils.get_first_param(request, 'from')
    elif 'to' in geo_type:
        geo_place = html_utils.get_first_param(request, 'to')

    ret_val = call_geocoder(request, geo_place, geo_type)
    return ret_val

@view_config(route_name='planner_mobile', renderer='mobile/planner.html')
@view_config(route_name='planner_desktop', renderer='desktop/planner.html')
def planner(request):
    return request.model.get_plan(request.query_string, **request.params)

    ret_val = {}

    has_from_coord = html_utils.get_first_param_is_a_coord(request, 'fromCoord')
    has_to_coord   = html_utils.get_first_param_is_a_coord(request, 'toCoord')
    if has_from_coord and has_to_coord:
        ret_val = request.model.get_plan(request.query_string, **request.params)
    else:
        #import pdb; pdb.set_trace()
        ret_val = make_subrequest(request, '/planner_geocode.html', extra_params='geo_type=to' if has_from_coord else 'geo_type=from')
    return ret_val


@view_config(route_name='planner_walk_mobile', renderer='mobile/planner_walk.html')
@view_config(route_name='planner_walk_desktop', renderer='desktop/planner_walk.html')
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
def stop(request):
    stop   = request.model.get_stop(request.query_string, **request.params)
    ret_val = {}
    ret_val['stop'] = stop
    return ret_val

@view_config(route_name='stop_schedule_mobile', renderer='mobile/stop_schedule.html')
@view_config(route_name='stop_schedule_desktop', renderer='desktop/stop_schedule.html')
def stop_schedule(request):
    stop_id = html_utils.get_first_param(request, 'stop_id')
    route   = html_utils.get_first_param(request, 'route')
    url = 'stop_schedule.html?stop_id={0}&route={1}'.format(stop_id, route)

    ret_val = html_utils.service_tabs(request, url)
    ret_val['stop'] = request.model.get_stop_schedule(request.query_string, **request.params)
    return ret_val

@view_config(route_name='stop_select_form_mobile_short', renderer='mobile/stop_select_form.html')
@view_config(route_name='stop_select_form_mobile',       renderer='mobile/stop_select_form.html')
@view_config(route_name='stop_select_form_desktop',      renderer='desktop/stop_select_form.html')
def stop_select_form(request):
    ret_val = {}
    ret_val['place']  = html_utils.get_first_param(request, 'place')
    ret_val['routes'] = request.model.get_routes(request.query_string, **request.params)
    return ret_val

@view_config(route_name='stop_select_list_mobile', renderer='mobile/stop_select_list.html')
@view_config(route_name='stop_select_list_desktop', renderer='desktop/stop_select_list.html')
def stop_select_list(request):
    ret_val = {}
    route = html_utils.get_first_param(request, 'route')
    ret_val['route_stops'] = request.model.get_route_stops(request.query_string, **request.params)
    return ret_val

@view_config(route_name='stop_select_geocode_mobile', renderer='mobile/stop_select_geocode.html')
@view_config(route_name='stop_select_geocode_desktop', renderer='desktop/stop_select_geocode.html')
def stop_select_geocode(request):
    place = html_utils.get_first_param(request, 'place')
    ret_val = call_geocoder(request, place)
    return ret_val


@view_config(route_name='stops_near_mobile', renderer='mobile/stops_near.html')
@view_config(route_name='stops_near_desktop', renderer='desktop/stops_near.html')
def stops_near(request):
    ret_val = {}

    #import pdb; pdb.set_trace()
    def call_near_ws(geo=None):
        #import pdb; pdb.set_trace()
        p = Place.make_from_request(request)
        p.update_values_via_dict(geo)
        params = p.to_url_params()
        ret_val['place']   = p.__dict__
        ret_val['params']  = params
        num = 5
        if html_utils.get_first_param(request, 'show_more', None):
            num = 30
        params = "num={0}&{1}".format(num, params)
        ret_val['nearest'] = request.model.get_stops_near(params, **request.params)

    has_geocode = html_utils.get_first_param_as_boolean(request, 'has_geocode')
    has_coord   = html_utils.get_first_param_is_a_coord(request, 'placeCoord')
    if has_geocode or has_coord:
        call_near_ws()
    else:
        place = html_utils.get_first_param(request, 'place')
        geo = call_geocoder(request, place)

        if geo['count'] == 1:
            single_geo = geo['geocoder_results'][0]
            if single_geo['type'] == 'stop':
                query_string = "{0}&stop_id={1}".format(request.query_string, single_geo['stop_id'])
                ret_val = make_subrequest(request, '/stop.html', query_string)
            else:
                call_near_ws(single_geo)
        else:
            ret_val = make_subrequest(request, '/stop_select_geocode.html')

    return ret_val


@view_config(route_name='map_place_mobile', renderer='mobile/map_place.html')
@view_config(route_name='map_place_desktop', renderer='desktop/map_place.html')
def map_place(request):
    ret_val = {}
    p = Place.make_from_request(request)
    ret_val['place'] = p.__dict__
    return ret_val

def is_mobile(request):
    return '/m/' in request.path_url

def get_path(request, path):
    ret_val = path
    if is_mobile(request):
        ret_val = '/m' + path
    return ret_val

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


@view_config(route_name='sparkline_desktop')
@view_config(route_name='sparkline_mobile')
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
def adverts(request):
    ret_val = {}
    ret_val['bus_adverts']     = request.model.get_adverts("mode=bus&_LOCALE_=en",  **request.params)
    ret_val['bus_adverts_es']  = request.model.get_adverts("mode=bus&_LOCALE_=es",  **request.params)
    ret_val['rail_adverts']    = request.model.get_adverts("mode=rail&_LOCALE_=en", **request.params)
    ret_val['rail_adverts_es'] = request.model.get_adverts("mode=rail&_LOCALE_=es", **request.params)
    return ret_val


@view_config(route_name='index_desktop', renderer='index.html')
@view_config(route_name='index_mobile',  renderer='index.html')
def index_view(request):
    auth = "True"
    perm = "True"
    return {'authenticated':auth, 'authorized':perm}


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    '''
       what do i do?

       1. I'm called at startup of the Pyramid app.  
       2. I could be used to make db connection (pools), etc...
    '''
    log.info('Starting pyramid server...')


MODEL_GLOBAL = None
def get_model():
    ''' @see make_views() below, which should have a model passed in to configure the model global 
    '''
    global MODEL_GLOBAL
    if MODEL_GLOBAL is None:
        # TODO ... this right?
        # TODO ... better way to attach this to view?
        # TODO ... multi-threading/
        # do something to create a model...
        MODEL_GLOBAL = Model()
    return MODEL_GLOBAL


@subscriber(NewRequest)
def new_request_subscriber(event):
    '''
       what do i do?

       1. entry point for a new server request
       2. configure the request context object (can insert new things like db connections or authorization to pass around in this given request context)
    '''
    log.debug("new request called -- request is 'started'")
    request = event.request
    request.model = get_model()
    settings = request.registry.settings
    request.add_finished_callback(cleanup)


def cleanup(request):
    '''
       what do i do?

       1. I was configured via the new_request_subscriber(event) method
       2. I'm called via a server event (when a request is 'finished')
       3. I could do random cleanup tasks like close database connections, etc... 
    '''
    log.debug("cleanup called -- request is 'finished'")


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    '''
        render the notfound.mako page anytime a request comes in that 
        the app does't have mapped to a page or method
    '''
    return {}

