import os
import logging

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.response import Response
from pyramid.config import Configurator



log = logging.getLogger(__file__)
log.setLevel(logging.INFO)


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


@view_config(route_name='stop', renderer='desktop/stop.html')
def destop_stop_view(request):
    '''
       what do i do?

       1. query db service for this stop's info
       2. ...
    '''
    ret_val = {}
    stop_id = get_first_param_as_int(request, 'stop_id')

    if stop_id is not None:
        pass

    log.info(ret_val)
    return ret_val


@view_config(route_name='mstop', renderer='mobile/stop.html')
def mobile_stop_view(request):
    '''
       what do i do?

       1. query db service for this stop's info
       2. ...
    '''
    ret_val = {}
    stop_id = get_first_param_as_int(request, 'stop_id')

    if stop_id is not None:
        pass

    log.info(ret_val)
    return ret_val




def get_first_param_as_int(request, name, def_val=None):
    '''
        utility function
    '''
    ret_val=get_first_param(request, name, def_val)
    try:
        ret_val = int(ret_val)
    except:
        pass

    return ret_val


def get_first_param(request, name, def_val=None):
    '''
        utility function

        @return the first value of the named http param (remember, http can have multiple values for the same param name), 
        or def_val if that param was not sent via HTTP
    '''
    ret_val=def_val
    try:
        ret_val = request.params.getone(name)
    except:
        pass

    return ret_val


def make_views(config):
    ''' adds the views (see below) and static directories to pyramid's config
        TODO: is there a better way to dot this (maybe via an .ini file)
    '''
    # important ... allow .html extension on mako templates
    config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")


    # routes setup
    config.add_route('index',  '/')
    config.add_route('stop',   '/stop')
    config.add_route('mstop',  '/mobile/stop')

    here = os.path.dirname(os.path.abspath(__file__))
    config.add_static_view('css',    os.path.join(here, 'static/css'))
    config.add_static_view('js',     os.path.join(here, 'static/js'))
    config.add_static_view('images', os.path.join(here, 'static/images'))

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
