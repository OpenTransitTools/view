import logging
log = logging.getLogger(__file__)

import StringIO

from pyramid.response import Response
from pyramid.view import view_config

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated

import ott.view.view.desktop
import ott.view.view.mobile

from ott.view.model import Model
from ott.view.model_mock import ModelMock

import ott.view.utils.html_utils as html_utils
from ott.view.view.spark import sparkline_smooth



MODEL_GLOBAL = None
def get_model():
    ''' @see make_views() below, which should have a model passed in to configure the model global 
    '''
    global MODEL_GLOBAL
    if MODEL_GLOBAL is None:
        # do something to create a model...
        MODEL_GLOBAL = ModelMock()

    return MODEL_GLOBAL


def do_view_config(config):
    ''' adds the views (see below) and static directories to pyramid's config
        TODO: is there a better way to dot this (maybe via an .ini file)
    '''

    # routes setup
    config.add_route('index',                 '/')
    config.add_route('tracker_desktop',       '/arrivals')

    config.add_route('sparkline',             '/sparkline')

    config.add_route('stop_desktop',          '/stop.html')
    config.add_route('find_stop_desktop',     '/find_stop.html')
    config.add_route('route_stop_desktop',    '/route_stop_list.html')
    config.add_route('stop_schedule_desktop', '/stop_schedule.html')
    config.add_route('stop_geocode_desktop',  '/stop_geocode.html')

    config.add_route('exception_desktop',     '/exception.html')
    config.add_route('planner_form_desktop',  '/planner_form.html')
    config.add_route('planner_itin_desktop',  '/planner.html')

    config.add_route('feedback_desktop',      '/feedback.html')

    config.add_route('find_stop_mobile',      '/mobile/find_stop.html')
    config.add_route('stop_mobile',           '/mobile/stop.html')
    config.add_route('feedback_mobile',       '/mobile/feedback.html')


@view_config(route_name='sparkline')
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


@view_config(route_name='index', renderer='index.html')
def index_view(request):
    '''
       what do i do?

       1. check authentication / authorization 
       2. if not authenticated, ...
       3. if not authenticated ...
    '''
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

