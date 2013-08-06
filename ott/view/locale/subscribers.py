# TODO: how to do this via .ini file
import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

''' From http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/templates/mako_i18n.html
    orig (http://blog.abourget.net/2011/1/13/pyramid-and-mako:-how-to-do-i18n-the-pylons-way/)
'''
from pyramid.i18n import get_localizer, TranslationStringFactory

def is_between_zero_one(f):
    ''' check string, int, float for a numeric value 0 > and <= 1 '''
    ret_val = False
    try:
        if isinstance(f, (int, long, float)) and f > 0 and f <= 1:
            ret_val = True
        elif isinstance(f, (str, basestring, unicode)) and f.isdigit():
            f = float(f)
            if f > 0.0 and f <= 1.0:
                ret_val = True
    except Exception, e:
        log.warn(e)
    return ret_val

def is_fraction_of_one(f):
    ''' check to see if a string looks like a fraction with numbers on either side '''
    ret_val = False
    try:
        s = f.split('/')
        if len(s) == 2 and s[0].isdigit() and s[1].isdigit():
            ret_val = True
    except:
        pass
    return ret_val


def add_renderer_globals(event):
    request = event['request']
    event['_'] = request.translate
    event['localizer'] = request.localizer

#tf = TranslationStringFactory('YOUR_GETTEXT_DOMAIN')
tsf = TranslationStringFactory('controller')
def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)
    def auto_translate(*args, **kwargs):
        """ Calls Babel to translate strings, etc...
            @see: https://github.com/Pylons/pyramid_cookbook/blob/master/templates/mako_i18n.rst
            @see: http://docs.pylonsproject.org/projects/translationstring/en/latest/tstrings.html
            @see: http://pylonsbook.com/en/1.1/internationalization-and-localization.html
            @see: http://www.gnu.org/software/gettext/manual/gettext.html#Plural-forms

            NOTE Special code to handle 2 plural forms (only way I could figure out how to do plurals)

            ${_('singular', 'plural', mapping={'number':1})}

            msgid "singular"
            msgstr "Singular ${number}"

            msgid "plural"
            msgstr "Plural ${number}"
        """
        # if template has plurals of this form ${_('singular', 'plural', mapping={'number':1})}
        if len(args) == 2:
            # step 1: expect 2 strings - singular & plural .po entries 
            a = tsf(args[0])
            b = tsf(args[1])
            m = None
            n = 0  # singular / plural by default 1==singular, any other number is plural
            # step 2a: find any mapping passed in 
            if 'mapping' in kwargs:
                m = kwargs['mapping']
                # step 2b: find number indicating singular / plural
                if 'number' in m:
                    n = m['number']
                    if is_between_zero_one(n) or is_fraction_of_one(n):
                        n = 1   # trigger singular
                    else:
                        n = 111 # trigger plural

            # step 3: first step of two pass translation, finding out which .po string to use based on N
            p = localizer.pluralize(a, b, n)

            # step 4: second step of two pass translation, translating that string
            t = localizer.translate(p, 'view', m)
        else:
            f = tsf(*args, **kwargs)
            m = None if 'mapping' not in kwargs else kwargs['mapping']
            t = localizer.translate(f, 'view', m)
        return t

    request.localizer = localizer
    request.translate = auto_translate
