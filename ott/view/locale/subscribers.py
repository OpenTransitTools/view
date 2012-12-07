# TODO: how to do this via .ini file
import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

''' From http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/templates/mako_i18n.html
    orig (http://blog.abourget.net/2011/1/13/pyramid-and-mako:-how-to-do-i18n-the-pylons-way/)
'''
from pyramid.i18n import get_localizer, TranslationStringFactory


def add_renderer_globals(event):
    request = event['request']
    event['_'] = request.translate
    event['localizer'] = request.localizer

tsf = TranslationStringFactory('view')
def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)
    def auto_translate(*args, **kwargs):
        f = tsf(*args, **kwargs)
        t = localizer.translate(f, 'view')
        return t
    request.localizer = localizer
    request.translate = auto_translate
