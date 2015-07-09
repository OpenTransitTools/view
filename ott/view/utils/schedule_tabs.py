import logging
log = logging.getLogger(__file__)

import datetime

from ott.utils import date_utils
from ott.utils import html_utils
from ott.view.locale.subscribers import get_translator

def ret_me(s):
    return s
_ = ret_me

MORE=_('more')
TODAY=_('Today')


def use_previous_day(request):
    ''' rules to show previous date vs. today's date.  the problem is that 2am is yesterday
        in transit data terms, so show customer yesterday's data for early morning queries
    '''
    ret_val = False
    if date_utils.get_hour() < 33:
        day = html_utils.get_first_param_as_int(request, 'day')
        if day is None:
            ret_val = True
    return ret_val

def get_tabs(request, url):
    '''
    '''
    #import pdb; pdb.set_trace()
    is_prev_day = use_previous_day(request)
    if is_prev_day:
        date = date_utils.get_day_before()
    else:
        date  = html_utils.get_first_param_as_date(request)
        month = html_utils.get_first_param_as_int(request, 'month')
        day   = html_utils.get_first_param_as_int(request, 'day')
        date  = date_utils.set_date(date, month, day)

    more   = html_utils.get_first_param(request, 'more')
    tab_id = html_utils.get_first_param_as_int(request, 'tab_id', 0)


    ret_val = {}
    ret_val['more_form']   = date_utils.get_day_info(date)
    ret_val['pretty_date'] = date_utils.pretty_date(date)
    ret_val['tabs'] = get_svc_date_tabs(date, url, is_prev_day, tab_id, more is not None, get_translator(request))

    return ret_val

def make_tab_obj(name, id, date=None, uri=None, append=None):
    ''' for the date tab on the stop schedule page, we expect an object that has a name and a url
        this method builds that structure, and most importantly, the url for those tabs
    '''
    ret_val = {}

    # put the name of the tab first (and strip off any leading / trailing ZEROs if the name is a date)
    ret_val['name'] = name.lstrip('0').replace('/0','/')
    ret_val['date'] = date
    ret_val['tooltip'] = date_utils.pretty_date(date)
    ret_val['dow'] = date_utils.dow(date)
    ret_val['dow_abbrv'] = date_utils.dow_abbrv(date)

    # next give the tab object a URL ... date is broken up into month and day parts 
    if uri:
        month = ""
        day = ""
        tab_id = ""
        if date:
            month = "&month={0}".format(date.month)
            day = "&day={0}".format(date.day)
        if id:
            tab_id = "&tab_id={0}".format(id)

        ret_val["url"] = "{0}{1}{2}{3}".format(uri, month, day, tab_id)
        if append:
            ret_val["url"] = "{0}&{1}".format(ret_val["url"], append)

    return ret_val

def get_svc_date_tabs(dt, uri, is_prev_day, tab_id, highlight_more_tab=False, translate=ret_me, fmt='%m/%d/%Y', smfmt='%m/%d', pttyfmt='%A, %B %d, %Y'):
    ''' return 3 date strings representing the next WEEKDAY, SAT, SUN
    '''
    ret_val = []

    # step 0: save off today as well as some other calculations
    today = datetime.date.today()
    more_date = today
    if tab_id < 0 or tab_id is None:
        tab_id = 0
    if tab_id > 3:
        tab_id = 3


    # step 3: we have to get three date tabs that sit between TODAY and MORE tabs
    dates = ['j','u','n','k']
    dates[tab_id] = dt
    for i, d in enumerate(dates):
        if i == tab_id:
            continue
        dates[i] = dt + datetime.timedelta(days=i - tab_id)

    # step 4: create the date tabs
    do_highlight = not highlight_more_tab
    tabs = []
    for i, d in enumerate(dates):
        if d == today and not is_prev_day:
            name = translate(TODAY)
        else:
            name = d.strftime(smfmt)

        if do_highlight and d == dt:
            tabs.append(make_tab_obj(name, i, d))
        else:
            tabs.append(make_tab_obj(name, i, d, uri))

    # step 5: add the WEEKDAY, SATURDAY, SUNDAY tabs after the TODAY tab
    ret_val.extend(tabs)

    # step 6: show the 'more' tab ... either highlighted or not
    more_tab = None
    more_title = translate(MORE)
    if highlight_more_tab:
        more_tab = make_tab_obj(more_title, tab_id)  # the more tab is highlighted
    else:
        more_tab = make_tab_obj(more_title, tab_id, more_date, uri, MORE)
    more_tab['tooltip'] = more_title
    ret_val.append(more_tab)

    return ret_val

def old_get_svc_date_tabs(dt, uri, highlight_more_tab=False, translate=ret_me, fmt='%m/%d/%Y', smfmt='%m/%d', pttyfmt='%A, %B %d, %Y'):
    ''' return 3 date strings representing the next WEEKDAY, SAT, SUN
    '''
    ret_val = []

    # step 0: save off today as well as some other calculations
    today = datetime.date.today()
    is_today = today == dt
    more_date = dt

    # step 1: if we're dealing with today, increment the date to show other dates in tabs to right
    if is_today:
        offset = 1
        # step 1b: if this is a weekday, increment to following Monday
        if dt.weekday() < 5:
            offset = 7 - dt.weekday()
        dt = dt + datetime.timedelta(days=offset)

    # step 2: make the 'today' tab...
    if is_today and not highlight_more_tab:
        ret_val.append(make_tab_obj(translate(TODAY), today))  # TODAY tab is highlighted
    else:
        ret_val.append(make_tab_obj(translate(TODAY), today, uri, ))

    # step 3: we have to get three date tabs that sit between TODAY and MORE tabs
    #         we'll create a WEEKDAY, SATURDAY and SUNDAY tabs ...
    #         the position of these relative date tabs is depentent upon TODAY's day of week...
    dates = ['WEEKDAY', 'SATURDAY', 'SUNDAY']
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
            dates[0] = dt - datetime.timedelta(days=1)  # Prev Saturday
            dates[1] = dt                               # Sunday
            dates[2] = dt + datetime.timedelta(days=1)  # Next Monday
        else:
            last_sat = dt.weekday() + 2
            last_sun = dt.weekday() + 1
            dates[0] = dt - datetime.timedelta(days=last_sat)  # Last Saturday
            dates[1] = dt - datetime.timedelta(days=last_sun)  # Last Sunday
            dates[2] = dt                                      # Weekday


    # step 4: create the WEEKDAY, SATURDAY, SUNDAY tabs
    do_highlight = not is_today and not highlight_more_tab
    tabs = []
    for d in dates:
        if do_highlight and d == dt:
            tabs.append(make_tab_obj(d.strftime(smfmt), d))
        else:
            tabs.append(make_tab_obj(d.strftime(smfmt), d, uri))

    # step 5: add the WEEKDAY, SATURDAY, SUNDAY tabs after the TODAY tab
    ret_val.extend(tabs)

    # step 6: show the 'more' tab ... either highlighted or not
    more_tab = None
    more_title = translate(MORE)
    if highlight_more_tab:
        more_tab = make_tab_obj(more_title)  # the more tab is highlighted
    else:
        more_tab = make_tab_obj(more_title, more_date, uri, MORE)
    more_tab['tooltip'] = more_title
    ret_val.append(more_tab)

    return ret_val

