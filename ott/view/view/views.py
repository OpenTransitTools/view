import os
import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

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


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    '''
        render the notfound.mako page anytime a request comes in that 
        the app does't have mapped to a page or method
    '''
    return {}


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
    log.info('Starting pyramid server -- visit me on http://localhost:8080')


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


MODEL_GLOBAL = None
def get_model():
    ''' @see make_views() below, which should have a model passed in to configure the model global 
    '''
    global MODEL_GLOBAL
    if MODEL_GLOBAL is None:
        # do something to create a model...
        MODEL_GLOBAL = {}

    return MODEL_GLOBAL


def make_views(config, model):
    ''' adds the views (see below) and static directories to pyramid's config
        TODO: is there a better way to dot this (maybe via an .ini file)
    '''

    # set the global model to this mod
    global MODEL_GLOBAL
    MODEL_GLOBAL = model

    # important ... allow .html extension on mako templates
    config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")

    # routes setup
    config.add_route('index',                 '/')
    config.add_route('tracker_desktop',       '/arrivals')

    config.add_route('stop_desktop',          '/stop.html')
    config.add_route('find_stop_desktop',     '/find_stop.html')
    config.add_route('route_stop_desktop',    '/route_stop_list.html')
    config.add_route('stop_schedule_desktop', '/stop_schedule.html')
    config.add_route('stop_geocode_desktop',  '/stop_geocode.html')

    config.add_route('feedback_desktop',      '/feedback.html')



    config.add_route('find_stop_mobile',      '/mobile/find_stop.html')
    config.add_route('stop_mobile',           '/mobile/stop.html')
    config.add_route('feedback_mobile',       '/mobile/feedback.html')

    here   = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.abspath(os.path.join(here, os.path.pardir))
    images = os.path.join(parent, 'static/images')
    config.add_static_view('images', images)

    config.scan()


def make_config(settings):
    ''' make the config 
    '''
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['pyramid.default_locale_name'] = 'en'

    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)

    # internationalization ... @see: locale/subscribers.py for more info
    config.add_translation_dirs('ott.view:locale')
    config.add_subscriber('ott.view.locale.subscribers.add_renderer_globals', 'pyramid.events.BeforeRender')
    config.add_subscriber('ott.view.locale.subscribers.add_localizer', 'pyramid.events.NewRequest')

    return config

