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

import ott.view.view.desktop
import ott.view.view.mobile

from ott.view.model import Model
from ott.view.model_mock import ModelMock
model = ModelMock()

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


def make_views(config):
    ''' adds the views (see below) and static directories to pyramid's config
        TODO: is there a better way to dot this (maybe via an .ini file)
    '''
    # important ... allow .html extension on mako templates
    config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")


    # routes setup
    config.add_route('index',  '/')
    config.add_route('find_stop', '/find_stop')
    config.add_route('mfind_stop', '/mobile/find_stop')

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
