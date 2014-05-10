import logging
log = logging.getLogger(__file__)

import datetime
import time
from calendar import monthrange

import date_utils
import html_utils
from ott.view.locale.subscribers import get_translator

def ret_me(s):
    return s
_ = ret_me

MORE=_('more')
TODAY=_('Today')

def get_tabs(request, url):
    '''
    '''
    date  = html_utils.get_first_param_as_date(request)
    month = html_utils.get_first_param_as_int(request, 'month')
    day   = html_utils.get_first_param_as_int(request, 'day')
    date  = date_utils.set_date(date, month, day)
    more  = html_utils.get_first_param(request, 'more')

    ret_val = {}
    ret_val['more_form']   = date_utils.get_day_info(date)
    ret_val['pretty_date'] = date_utils.pretty_date(date)
    ret_val['tabs'] = get_svc_date_tabs(date, url, more is not None, get_translator(request)) 

    return ret_val


def make_tab_obj(name, uri=None, date=None, append=None):
    ''' for the date tab on the stop schedule page, we expect an object that has a name and a url
        this method builds that structure, and most importantly, the url for those tabs
    '''
    ret_val = {}

    # put the name of the tab first (and strip off any leading / trailing ZEROs if the name is a date)
    ret_val["name"] = name.lstrip('0').replace('/0','/')

    # next give the tab object a URL ... date is broken up into month and day parts 
    if uri:
        month = ""
        day = ""
        if date:
            month = "&month={0}".format(date.month)
            day = "&day={0}".format(date.day)
        ret_val["url"] = "{0}{1}{2}".format(uri, month, day)
        if append:
            ret_val["url"] = "{0}&{1}".format(ret_val["url"], append)

    return ret_val


def get_svc_date_tabs(dt, uri, highlight_more_tab=False, translate=ret_me, fmt='%m/%d/%Y', smfmt='%m/%d', pttyfmt='%A, %B %d, %Y'):
    ''' return 3 date strings representing the next WEEKDAY, SAT, SUN 
    '''
    ret_val = []

    #import pdb; pdb.set_trace()

    # step 1: make the 'today' tab...
    if datetime.date.today() == dt and not highlight_more_tab:
        ret_val.append(make_tab_obj(translate(TODAY)))  # TODAY tab is highlighted
    else:
        ret_val.append(make_tab_obj(translate(TODAY), uri, datetime.date.today()))

    #ret_val.append(make_tab_obj(dt.strftime(smfmt)))

    # step 2: figure out how many days from target is next sat, sunday and/or monday (next two service days different from today)
    delta1 = 1
    delta2 = 2
    if dt.weekday() < 5:
        # date is a m-f, so we're looking for next sat (delta1) and sun (delta 2)
        delta1 = 5 - dt.weekday()
        delta2 = delta1 + 1
    elif dt.weekday() == 6:
        # date is a sunday, so we're looking for monday (delta1), which is = 1 day off, and next sat (delta2) which is +6 days off 
        delta2 = 6

    d1 = dt + datetime.timedelta(days=delta1)
    d2 = dt + datetime.timedelta(days=delta2)
    #print "{0} {1} {2}={3} {4}={5}".format(dt, dt.weekday(), delta1, d1, delta2, d2)

    # step 3: add the next to service day tabs to our return array
    ret_val.append(make_tab_obj(d1.strftime(smfmt), uri, d1))
    ret_val.append(make_tab_obj(d2.strftime(smfmt), uri, d2))

    # TODO put the ret_val appen stuff in a separte method that builds up the dict...
    #      and add a pretty_date to that dict, so that we can create a css TOOLTIP that shows what weekday / date the 2/1, 2/5, 2/6 dates represent...
    #, "pretty_date": pretty_date(d1, pttyfmt)})

    # step 4: show the 'more' tab ... either highlighted or not
    if highlight_more_tab:
        ret_val.append(make_tab_obj(translate(MORE)))  # the more tab is highlighted
    else:
        ret_val.append(make_tab_obj(translate(MORE), uri, dt, MORE))

    return ret_val

