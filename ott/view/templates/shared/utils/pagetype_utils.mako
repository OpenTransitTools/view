## -*- coding: utf-8 -*-
##
## these methods control the page background (css file), the name of the page, any links in that name, etc...
##
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>

## css include controls the page look
<%def name="stop_css()"></%def>
<%def name="tripplanner_css()"></%def>

<%def name="base_stop_stations(name, extra_params, base_params, ele_type='div')">
##    <div class="standardheader">
##        <h1 class="stopsstationsh1"><a href="stop_select_form.html?${base_params}${extra_params}"><i class="tmfa-ss-outline h1icon"></i></a> ${_(u'Stops & Stations')}</h1>
##    </div><!-- .standardheader -->
</%def>

##
## for stop & station pages that only show the basic header (no specific stop info / alerts / etc...)
##
<%def name="stop_select(name='', extra_params='', base_params='me', ele_type='div')">
    ${base_stop_stations(name, extra_params, base_params, ele_type)}
    <h2>Select a ${name} stop</h2>
</%def>

##
## for stop & station pages that have specific stop info (ala alerts / stop landing page link / etc...)
##
<%def name="stop(name='', extra_params='', base_params='me', stop=None, has_alerts=False)">
    ${base_stop_stations(name, extra_params, base_params)} 
   ## <h2>${name}</h2>
</%def>

#
# for stop schedule pages that have specific stop info (ala alerts / stop landing page link / etc...)
#
<%def name="stop_schedule(name='', extra_params='', base_params='me', stop=None, has_alerts=False)">
    ${base_stop_stations(name, extra_params, base_params)}
    <a href="stop.html?${request.query_string}">${name}</a>
    %if has_alerts is True:
    ${util.alerts_inline_icon_link()}
    %endif
</%def>


#
# trip planner pages
#

<%def name="trip_planner(name='', extra_params='', base_params='me', is_mobile=False)">
%if not is_mobile:
%endif

</%def>

<%def name="trip_planner_form(name='', extra_params='', base_params='me')">
    <div class="standardheader">
        <h1><a href="planner_form.html?${base_params}${extra_params}">${_(u'Trip Planner')}</a></h1>
    </div><!-- .standardheader --> 
</%def>


