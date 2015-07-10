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
    if date_utils.get_hour() < 3:
        day = html_utils.get_first_param_as_int(request, 'day')
        if day is None:
            ret_val = True
    return ret_val

def get_tabs(request, url):
    ''' make the set of tabs on the schedule page
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
    ret_val['tabs'] = make_date_tabs(date, url, is_prev_day, tab_id, more is not None, get_translator(request))

    return ret_val

def make_date_tabs(date, uri, is_prev_day, tab_id, highlight_more_tab=False, translate=ret_me, fmt='%m/%d/%Y', smfmt='%m/%d', pttyfmt='%A, %B %d, %Y'):
    ''' return our set 4 date tabs and the more tab
    '''

    # step 1: save off today as well as some other calculations
    today = datetime.date.today()
    more_date = today

    # step 2: make sure our tab index is a number between 0 and 3
    if tab_id is None or not isinstance(tab_id, int) or tab_id < 0:
        tab_id = 0
    if tab_id > 3:
        tab_id = 3

    # step 3: we have to make an array of 4 dates that surround the input dt dated
    dates = ['d','a','n','k']
    for i, d in enumerate(dates):
        if i == tab_id:
            # step 3a: this is the input date, put into the tab_id slot
            dates[tab_id] = date
        else:
            # step 3b: offset our date by x days for the other tabs (can be negative offset when tab_id > 0)
            offset = i - tab_id
            dates[i] = date + datetime.timedelta(days=offset)

    # step 4: create the date tabs
    tabs = []
    for i, d in enumerate(dates):
        # step 4a: create the name of the tab (sometimes we use 'TODAY', and sometimes just the date is the name)
        if d == today and not is_prev_day:
            name = translate(TODAY)
        else:
            name = d.strftime(smfmt)

        # step 4b: make the tab clickable whenever the more tab is clickable, or when this date is the target date
        if highlight_more_tab or d != date:
            tabs.append(make_tab_obj(name, i, d, uri))
        else:
            tabs.append(make_tab_obj(name, i, d))

    # step 5: show the 'more' tab ... either highlighted or not
    more_title = translate(MORE)
    if highlight_more_tab:
        more_tab = make_tab_obj(more_title, 0)  # the more tab is highlighted
    else:
        more_tab = make_tab_obj(more_title, 0, more_date, uri, MORE)
    more_tab['tooltip'] = more_title
    tabs.append(more_tab)

    return tabs

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
