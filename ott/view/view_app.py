import os
import logging

from wsgiref.simple_server import make_server

from ott.view.view.views import make_views
from ott.view.view.views import make_config

from ott.view.model import Model
from ott.view.model_mock import ModelMock
model = ModelMock()


# TODO: how to do this via .ini file
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)


def main():
    # configuration settings
    here = os.path.dirname(os.path.abspath(__file__))
    mako_dir = os.path.join(here, 'templates')
    log.info(here + " " + mako_dir)

    # make the mako views
    settings={}
    settings['mako.directories'] = mako_dir
    config=make_config(settings)
    make_views(config, model)


    # serve app
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
    get_settings()


if __name__ == '__main__':
    main()

