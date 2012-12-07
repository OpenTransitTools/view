import os
import logging

from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated

from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from wsgiref.simple_server import make_server

from ott.view.views import make_views

# TODO: how to do this via .ini file
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

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


def main():
    # configuration settings
    here = os.path.dirname(os.path.abspath(__file__))
    mako_dir = os.path.join(here, 'templates')
    log.info(here + " " + mako_dir)

    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['mako.directories'] = mako_dir
    settings['pyramid.default_locale_name'] = 'en'

    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)

    # internationalization ... @see: locale/subscribers.py for more info
    config.add_translation_dirs('ott.view:locale')
    config.add_subscriber('ott.view.locale.subscribers.add_renderer_globals', 'pyramid.events.BeforeRender')
    config.add_subscriber('ott.view.locale.subscribers.add_localizer', 'pyramid.events.NewRequest')

    make_views(config)

    # serve app
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
    get_settings()



if __name__ == '__main__':
    main()
