## -*- coding: utf-8 -*-
##
## routines for stop / stop_schedule pages
##
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>

<%def name="route_param(def_val='')"><%
    ret_val = def_val
    if 'route' in request.params:
        ret_val = request.params['route']
    if ret_val is None or ret_val == 'None':
        ret_val = def_val
    return ret_val
%></%def>


<%def name="sort_val()"><%
    sort_val = 'destination' if 'sort' in request.params and request.params['sort'] ==  'destination' else 'time'
    return sort_val
%></%def>

<%def name="sort_by_time()"><%
    sort_by_time = False if 'sort' in request.params and request.params['sort'] == 'destination' else True
    return sort_by_time
%></%def>


<%def name="make_stop_schedule_url(stop_id, sort, extra_params, all=False)"><%
    ## TODO: make the month/day/route variables more abstract, with better tests for None and '' values
    month  = '' if 'month' not in request.params else "&month={0}".format(request.params['month'])
    day    = '' if 'day'   not in request.params else "&day={0}".format(request.params['day'])
    route  = '' if all or 'route' not in request.params else "&route={0}".format(request.params['route'])
    url = "stop_schedule.html?stop_id={0}&sort={1}{2}{3}{4}{5}".format(stop_id, sort, route, month, day, extra_params)
    return url
%></%def>


##
## make name for the schedule tabs ... add dow (or abbrivated dow) to name the date named tabs (but not the 'Today' or 'more' tabs)
##
<%def name="make_tab_name(i, t)">
%if i==0 or i==4:
${t['name']}
%else:
${t['name']}<br/>${_(t['dow_abbrv'])}
%endif
</%def>

# TODO ... remove me once JH fixes the .css for month abbreviations 
<%def name="make_tab_name(i, t)">${t['name']}</%def>

##
## the crazy Today, 10/25, 10/26, more stuff from stop schedule pages
##
<%def name="svc_key_tabs(stop, html_tabs, extra_params)">
    <ul id="contenttabs" class="group">
        %for i, t in enumerate(html_tabs['tabs']):
          %if 'url' in t:
            <li class="normal"   title="${t['tooltip']}"><a href="${t['url']}&sort=${sort_val()}${extra_params}"><span>${make_tab_name(i, t)}</span></a></li>
          %else:
            <li class="selected" title="${t['tooltip']}"><span>${make_tab_name(i, t)}</span></li>
          %endif
        %endfor
    </ul>
    %if 'more' in request.params:
    <div id="moreform" class="group">
        <form name="select_date" id="select_date_id" method="GET" action="stop_schedule.html" class="triptools-form">
            ${form.get_extra_params_hidden_inputs()}
            <input type="hidden" name="route"   value="${route_param()}" />
            <input type="hidden" name="stop_id" value="${stop['stop_id']}" />
            <input type="hidden" name="sort"    value="${sort_val()}" />
            %if html_tabs['more_form']:
            ${util.month_select(html_tabs['more_form']['month'])} ${util.day_select(html_tabs['more_form']['day'])}
            <input name="submit" type="submit" value="${_(u'Select')}" class="submit" />
            %endif
        </form>
    </div>
    %endif
</%def>

##
## switch to show all routes if we're just showing a single route stop times...
##
<%def name="schedule_all_routes_link(ss, extra_params)">
<div class="contenttabs-bar group">
    <p class="singleroute">
    %if 'single_route_name' in ss and ss['single_route_name'] != None:
    <b>${_(u'Showing only')} ${ss['single_route_name']}</b>
     &nbsp;|&nbsp; <a href="${make_stop_schedule_url(ss['stop']['stop_id'], sort_val(), extra_params, True)}">${_(u'Show all lines')}</a>
    %endif
    </p>
</%def>

##
## sort schedule by either route (blocky view) or time (list view)
##
<%def name="schedule_sort_by_links(stop, extra_params)">
    <p class="sort">
        ${util.link_or_strong(_(u'Sorting by line'), _(u'Sort by line'), not sort_by_time(), make_stop_schedule_url(stop['stop_id'], 'destination', extra_params))}
         &nbsp;|&nbsp;
        ${util.link_or_strong(_(u'Sorting by time'), _(u'Sort by time'),  sort_by_time(),    make_stop_schedule_url(stop['stop_id'], 'time', extra_params))}
    </p>
</div><!-- end .contenttabs-bar -->
</%def>

##
## sort schedule by either route (blocky view) or time (list view)
##
<%def name="schedule_render(ss, pretty_date, extra_params, is_mobile=False)">
    %if len(ss['stoptimes']) > 0:
        ###
        ###  SHOW schedule as a list, with headsign to left of time...
        ###
        %if sort_by_time():
        <div class="sortbyline">
            %for s in ss['stoptimes']:
            <%
                id = s['h']
                hs = ss['headsigns'][id]
            %> 
            <p><b>${s['t']}</b> ${hs['route_name']} ${_(u'to')} ${hs['headsign']}</p>
            %endfor
        </div>

        ###
        ###  SHOW schedule grouped under headsign
        ###
        %else:
        <%
            hs_list = ss['headsigns'].values()
            hs_list.sort(key=lambda hs: hs['sort_order'], reverse=False)
        %>
        %for hs in hs_list:
        <h3 class="tight">
            ${hs['route_name']} ${_(u'to')} ${hs['headsign']}
            %if hs['has_alerts']:
            ${util.alerts_inline_icon_link()}
            %endif
        </h3>
        <p class="tight">
            %for s in ss['stoptimes']:
                %if s['h'] == hs['id']:
                ${s['t']}&nbsp; 
                %endif
            %endfor
        </p>
        <p>
            <%
               from ott.view.utils import agency_template
               url = agency_template.make_url_template()
            %>
            <a href="${url.get_arrivals_url(stop_id=hs['stop_id'], route_id=hs['route_id'], device=is_mobile)}">${_(u'Next arrivals')}</a>
        </p>
        %endfor
        %endif
    %else:
        ###
        ###  SHOW the No service message, since we don't have any stop times...
        ###
        <strong>${_(u'No service')}</strong> ${_(u'at this stop')} ${_(u'on')} ${pretty_date} 
        %if route_param(None):
            ${_(u'for')} ${_(u'line')} #${route_param()}
        %endif
    %endif
</%def>

