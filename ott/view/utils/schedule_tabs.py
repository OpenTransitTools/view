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
    today = datetime.date.today() 
    today = datetime.date(2014, 5, 11)
    is_today = today == dt

    
    if is_today:
        dt = dt + datetime.timedelta(days=1)

    # step 1: make the 'today' tab...
    if is_today and not highlight_more_tab:
        ret_val.append(make_tab_obj(translate(TODAY)))  # TODAY tab is highlighted
    else:
        ret_val.append(make_tab_obj(translate(TODAY), uri, today))

    dates = [None, None, None]
    if today.weekday() == 5:     # TODAY is a Saturday
        if dt.weekday() == 5:    # DATE is also Saturday
            dates[0] = dt - datetime.timedelta(days=6)  # Last Sunday
            dates[1] = dt - datetime.timedelta(days=5)  # Last Monday
            dates[2] = dt                               # Saturday
        elif dt.weekday() == 6:  # DATE is a Sunday
            dates[0] = dt                               # Sunday
            dates[1] = dt + datetime.timedelta(days=1)  # Monday
            dates[2] = dt + datetime.timedelta(days=6)  # Next Saturday
        else:                    # DATE is Weekday
            prev_sun = dt.weekday() + 1
            next_sat = 5 - dt.weekday()
            dates[0] = dt - datetime.timedelta(days=prev_sun)
            dates[1] = dt
            dates[2] = dt + datetime.timedelta(days=next_sat)
    elif today.weekday() == 6:  # TODAY is a Sunday
        if dt.weekday() == 6:   # DATE is also a Sunday
            dates[0] = dt - datetime.timedelta(days=6)  # Last Monday
            dates[1] = dt - datetime.timedelta(days=1)  # Last Saturday
            dates[2] = dt                               # Sunday 
        elif dt.weekday() == 5: # DATE is a Saturday
            dates[0] = dt - datetime.timedelta(days=5)  # Last Monday
            dates[1] = dt                               # Saturday
            dates[2] = dt + datetime.timedelta(days=1)  # Next Sunday
        else:                   # DATE is Weekday
            next_sat = 5 - dt.weekday()
            next_sun = next_sat+1
            dates[0] = dt
            dates[1] = dt + datetime.timedelta(days=next_sat)
            dates[2] = dt + datetime.timedelta(days=next_sun)
    else:                        # TODAY is a Weekday
        if dt.weekday() == 5:    # DATE is a Saturday
            dates[0] = dt                               # Saturday
            dates[1] = dt + datetime.timedelta(days=1)  # Next Sunday
            dates[2] = dt + datetime.timedelta(days=2)  # Next Monday
        elif dt.weekday() == 6:  # DATE is a Sunday
            dates[0] = dt - datetime.timedelta(days=1)  # Prev Sunday
            dates[1] = dt                               # Saturday
            dates[2] = dt + datetime.timedelta(days=1)  # Next Monday
        else: 
            # TODO compare 
            last_sat = 5 - dt.weekday()
            last_sun = last_sat+1
            dates[0] = dt - datetime.timedelta(days=last_sun)  # Last Sunday
            dates[1] = dt - datetime.timedelta(days=last_sat)  # Last Saturday
            dates[2] = dt                                      # Weekday


    # step 3: add the next to service day tabs to our return array
    tabs = []
    do_highlight = True
    if is_today or highlight_more_tab:
        do_highlight = False
    for d in dates:
        if do_highlight and d == dt:
            tabs.append(make_tab_obj(d.strftime(smfmt)))
        else:
            tabs.append(make_tab_obj(d.strftime(smfmt), uri, d))

    ret_val.extend(tabs)

    # TODO put the ret_val appen stuff in a separte method that builds up the dict...
    #      and add a pretty_date to that dict, so that we can create a css TOOLTIP that shows what weekday / date the 2/1, 2/5, 2/6 dates represent...
    #, "pretty_date": pretty_date(d1, pttyfmt)})

    # step 4: show the 'more' tab ... either highlighted or not
    if highlight_more_tab:
        ret_val.append(make_tab_obj(translate(MORE)))  # the more tab is highlighted
    else:
        ret_val.append(make_tab_obj(translate(MORE), uri, dt, MORE))

    return ret_val

