## -*- coding: utf-8 -*-
##
## routines for stop / stop_schedule pages
##
<%namespace name="util" file="/shared/utils/misc_util.mako"/>
<%namespace name="page" file="/shared/utils/pagetype_utils.mako"/>

<%def name="page_title(stop)">TriMet: ${_(u'Stop ID')} ${stop['stop_id']} - ${stop['name']}</%def>

<%def name="has_alerts(stop)"><%
    has_alerts = True if 'alerts' in stop and len(stop['alerts']) > 0 else False
    return has_alerts
%></%def>
<%def name="make_name_id(stop)"><%
    name = "{0} {1}".format(_(u'Stop ID').encode('utf-8'), stop['stop_id']).decode('utf-8')
    return name
%></%def>
<%def name="make_url_params(stop)"><%
    params = "stop&name={0}&lat={1}&lon={2}".format(stop['name'], stop['lat'], stop['lon'])
    return params
%></%def>


<%def name="planner_walk_link(from_place, to_stop)">
<a href="planner_walk.html?">${_(u'miles', to_stop['distance'])}</a>
</%def>

<%def name="route_abrv_list(stop)">
    %if stop and stop['routes']:
    %for i, r in enumerate(stop['routes']):
${', ' if (i > 0) else ''}<a target="#" href="${r['route_url']}">${r['short_name']}</a>
%endfor
%endif
</%def>

<%def name="routes_served(stop)">
 ${_(u'Served by')}: ${route_abrv_list(stop)}
</%def>
 