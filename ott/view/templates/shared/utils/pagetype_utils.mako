## -*- coding: utf-8 -*-
##
## these methods name of the page, any links in that name, etc...
##
<%namespace name="util" file="/shared/utils/misc_util.mako"/>

<%def name="h1_base_stop_stations(name, extra_params, base_params)">
    <h1 class="stopsstations-icon">
        <a href="stop_select_form.html?${base_params}${extra_params}" title="${_(u'Stops & Stations')} ${_(u'Home')}" class="homelink"><span class="visuallyhidden">${_(u'Stops & Stations')} ${_(u'Home')}</span></a>
</%def>
#
# for stop & station pages that only show the basic header (no specific stop info / alerts / etc...)
#
<%def name="stop_select(name='', extra_params='', base_params='me')">
    ${h1_base_stop_stations(name, extra_params, base_params)}
       ${name}
    </h1>
</%def>


#
# for stop & station pages that have specific stop info (ala alerts / stop landing page link / etc...)
#
<%def name="stop(name='', extra_params='', base_params='me', has_alerts=False, stop=None)">
    ${h1_base_stop_stations(name, extra_params, base_params)}
        %if stop:
        <a href="stop.html?stop_id=${stop['stop_id']}${extra_params}">${name}</a>
        %else:
        ${name}
        %endif
        %if has_alerts:
        ${util.alerts_inline_icon_link()}
        %endif
    </h1>
</%def>


<%def name="trip_planner(name='', extra_params='', base_params='me')">
</%def>

