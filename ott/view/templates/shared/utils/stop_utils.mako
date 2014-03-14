## -*- coding: utf-8 -*-
##
## routines for stop / stop_schedule pages
##
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="page" file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>

<%def name="page_title(stop)">TriMet: ${_(u'Stop ID')} ${stop['stop_id']} - ${stop['name']}</%def>
<%def name="str_title(stop)"><% return "Stop ID {0}".format(stop['stop_id']) %></%def>

##
## stop ambiguous geocode form(s) 
##
<%def name="geocode_form(geocoder_results, geo_place='', geo_type='place', form_action='stops_near.html', is_mobile=False)">
<div id="location">
    %if geocoder_results and len(geocoder_results) > 0:
    <form action="${form_action}"  method="GET" name="ambig" class="triptools-form">
        <style>select {width: 32em;}</style>
        ${form.has_geocode_hidden('true')}
        ${form.get_extra_params_hidden_inputs()}
        ${form.search_list(_(u'Select a location'), geocoder_results)}
    </form>
    %endif

    <form action="${form_action}"  method="GET" name="ambig" class="triptools-form">
        ${form.has_geocode_hidden('false')}
        ${form.get_extra_params_hidden_inputs()}
        ${form.search_input(_(u'Find stops and stations'), geo_place)}
        ${form.search_submit(_(u'Continue'))}
    </form>
</div>
</%def>

<%def name="has_alerts(stop)">
<%
    has_alerts = True if 'alerts' in stop and len(stop['alerts']) > 0 else False
    return has_alerts
%>
</%def>

<%def name="make_name_id(stop)">
<%
    name = "{0} {1}".format(_(u'Stop ID').encode('utf-8'), stop['stop_id']).decode('utf-8')
    return name
%>
</%def>

<%def name="make_url_params(stop)">
<%
    params = "stop&name={0}&lat={1}&lon={2}".format(stop['name'], stop['lat'], stop['lon'])
    return params
%>
</%def>

<%def name="planner_walk_link(frm, to, extra_params)">
<%
    dist = _('${number} mile', '${number} miles', mapping={'number':round(to['distance'], 2)})
%>
<a href="planner_walk.html?mode=WALK&from=${util.make_named_coord_from_obj(frm)}&to=${util.make_named_coord_from_obj(to)}${extra_params}">${dist}</a>
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

<%def name="nearby_stops_link(stop, extra_params)">
    <p><a href="stops_near.html?has_geocode=true&place=${util.make_named_coord_from_obj(stop)}${extra_params}">${_(u'Find nearby stops')}</a></p>
</%def>

## static map block
<%def name="static_map_img(map_url)"><img src="${map_url}" alt="${_(u'Stop location on a map')}"/></%def>

<%def name="imap_a_link(name, lon, lat, extra_params, imap_cls=False)"><a ${'class="imap"' if imap_cls else '' | n} target="#" href="http://ride.trimet.org/?zoom=16&pLat=${lat}&pLon=${lon}&pText=${name}${extra_params}" title="${_(u'View on Interactive Map')}"></%def>
<%def name="imap_a_link_via_stop(stop, extra_params, imap_cls=False)">${imap_a_link(stop['name'], stop['lon'], stop['lat'], extra_params, imap_cls)}</%def>


<%def name="staticmap_imap_link(name, lon, lat, extra_params, map_url)">
<p>
    ${imap_a_link(name, lon, lat, extra_params)}
        ${static_map_img(map_url)}
    </a>
</p>
<p>
    ${imap_a_link(name, lon, lat, extra_params, True)}
       <span class="imap-text">${_(u'View on Interactive Map')}</span><br /><span class="secondary">${_(u'High-speed connection recommended')}</span>
    </a>
</p>
</%def>

<%def name="map_and_links(map_url, name, lon, lat, extra_params, is_mobile)">
<%
    if is_mobile:
        static_map_img(map_url)
    else:
        staticmap_imap_link(name, lon, lat, extra_params, map_url)
%>
</%def>

## places map with lat/lon
<%def name="place_map(name, lon, lat, extra_params='', is_mobile=False)">
<%
    w=665
    h=350
    if is_mobile:
        w=300
        h=240
    map_url = "http://ride.trimet.org/eapi/ws/V1/mapimage/format/png/width/{0}/height/{1}/zoom/7/coord/{2},{3}/extraparams/f\
ormat_options=layout:scale".format(w, h, lon, lat)
    map_and_links(map_url, name, lon, lat, extra_params, is_mobile)
%>
</%def>

## stops map with lat/lon
<%def name="stop_map(name, stop_id, lon, lat, extra_params='', is_mobile=False)">
<%
    w=305
    h=290
    if is_mobile:
        w=300
        h=240
    map_url = "http://ride.trimet.org/eapi/ws/V1/stopimage/format/png/width/{0}/height/{1}/zoom/6/extraparams/format_options\
=layout:scale/id/{2}".format(w, h, stop_id)
    map_and_links(map_url, name, lon, lat, extra_params, is_mobile)
%>
