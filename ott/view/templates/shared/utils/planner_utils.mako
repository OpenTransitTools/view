## -*- coding: utf-8 -*-
##
## planner lib
##
<%namespace name="util"  file="/shared/utils/misc_utils.mako"/>

##
## typical itinerary page title
##
<%def name="itin_page_title(plan)">TriMet: ${_(u'Trip Planner')} - ${from_to_msg(plan)}</%def>

##
## @returns From <orig> to <dest>
##
<%def name="get_from_to(plan, def_val='')"><%
    ret_val = def_val
    try:
        if plan and 'from' in plan and 'to' in plan:
            ret_val = "{0} {1} {2} {3}".format(_(u'From'), plan['from']['name'], _(u'to'), plan['to']['name'])
    except:
        pass
    return ret_val
%></%def>

##
## @returns error['msg'] is that exits
##
<%def name="get_error_msg(error, def_val='')"><% return _(error['msg']) if error and 'msg' in error else def_val %></%def>

##
## if/else return for a decent page title
##
<%def name="from_to_msg(plan)"><%
    ret_val = get_from_to(plan, None)
    if ret_val is None:
        ret_val = get_error_msg(error, None)
    if ret_val is None:
        ret_val = _(u'Uncertain planner problem.')
    return ret_val
%></%def>

##
## string page title ... for feedback / emailing (mostly)
##
<%def name="str_title(plan)"><% from ott.utils import transit_utils; return transit_utils.plan_title(_(u'Trip Planner'), plan['from']['name'], _(u'to'), plan['to']['name'])%></%def>

##
## for feedback form ... briefly describe the trip request
##
<%def name="str_description(plan)"><% 
    title = str_title(plan)
    arr = get_depart_arrive(plan['params']['is_arrive_by'])
    opt = get_optimize(plan['params']['optimize'])
    from ott.utils import transit_utils;
    return transit_utils.plan_description(plan, title, arr, opt, _(u'using'), _(u'with a maximum walk of'))
%>
</%def> 

##
## header details w/ from & to details, plus optional trip details & edit links
##
<%def name="render_trip_details(plan, itinerary=None, extra_params='')">
    <div class="details">
        <p><b>${_(u'From')}</b> ${plan['from']['name']}</p>
        <p><b>${_(u'To')}</b> ${plan['to']['name']}</p>
        %if itinerary:
        <p><b>${_(u'When')}</b> ${itinerary['date_info']['pretty_date']}</p>
        <div class="tripinfo">
            <p>${get_depart_arrive_at(plan['params']['is_arrive_by'])} ${get_time(itinerary, plan['params']['is_arrive_by'])} ${itinerary['date_info']['pretty_date']}, ${_(u'using')} ${plan['params']['modes']} <a href="planner_form.html?${plan['params']['edit_trip']}${extra_params}" onclick="_gaq.push(['_trackEvent', 'TripPlanner', 'ClickTo', 'Itinerary edit top']);" class="hide">${_(u'Edit')}</a></p>
            <p>${get_optimize(plan['params']['optimize'])} ${_(u'with a maximum walk of')} ${plan['params']['walk']} <a href="planner_form.html?${plan['params']['edit_trip']}${extra_params}" onclick="_gaq.push(['_trackEvent', 'TripPlanner', 'ClickTo', 'Itinerary edit top']);" class="hide">${_(u'Edit')}</a></p>
        </div>
        %endif
    </div><!-- end #details -->
</%def>

##
## option tabs
##
<%def name="render_tabs(plan, extra_params)">
%if len(plan['itineraries']) > 1:
    <ol id="contenttabs" class="group">
        ${itin_tab(plan['itineraries'], 0, _(u'Best bet'), extra_params)}
        ${itin_tab(plan['itineraries'], 1, _(u'Option 2'), extra_params)}
        ${itin_tab(plan['itineraries'], 2, _(u'Option 3'), extra_params)}
    </ol><!-- end #tabs -->
%endif
</%def>

##
## main part of the renderer
## (loop over the legs, and render them
##
<%def name="render_itinerary(itinerary, extra_params, is_mobile=False, no_expand=False)">
    %if has_transit(itinerary):
    <ol id="itinerary" class="transit">
    %else:
    <ol id="itinerary" class="walkbike">
    <% no_expand=True %>
    %endif
        ##
        ## loop through the legs between start and end elements
        ## ${render_leg(leg, n)}
        %for n, leg in enumerate(itinerary['legs']):
            ${_render_leg(itinerary, n, is_mobile, extra_params, no_expand)}
        %endfor
    </ol><!-- end #itinerary -->
</%def>

##
## bottom console buttons for email, feedback, print, etc...
##
<%def name="render_console(plan, extra_params)">
    <div class="console">
        <div class="row">

            <div class="col-xs-12 col-sm-6 hcenter">
                <a href="${util.mailto_url(str_title(plan))}" class="console-emailtext" onClick="_gaq.push(['_trackEvent', 'TripPlanner', 'ClickTo', 'Itinerary email-text']);"><span>${_(u'Email/Text')}</span></a>
                <a href="javascript:window.print();" class="console-print" onClick="_gaq.push(['_trackEvent', 'TripPlanner', 'PrintClickTo', 'Itinerary print']);"><span>${_(u'Print')}</span></a>
            </div><!-- .col -->

            <div class="col-xs-12 col-sm-6 hcenter">
                <a href="planner_form.html?${plan['params']['return_trip']}${extra_params}" class="showalllines" onClick="_gaq.push(['_trackEvent', 'TripPlanner', 'ClickTo', 'Itinerary reverse']);"><span>${_(u'Return trip')}</span></a>
                <a href="planner_form.html?${plan['params']['edit_trip']}${extra_params}" class="showalllines" onClick="_gaq.push(['_trackEvent', 'TripPlanner', 'ClickTo', 'Itinerary edit']);"><span>${_(u'Edit/Start over')}</span></a>
            </div><!-- .col -->
        
        </div><!-- .row -->
    </div><!-- end #console -->

    <p><small>${_(u'Times shown are estimates based on schedules and can be affected by traffic, road conditions, detours and other factors. Before you go, check')}
        <a href="/transittracker/about.htm" onClick="_gaq.push(['_trackEvent', 'Trip Planner Ads','ClickTo', '/transittracker/about.htm']);">TransitTracker</a>&trade;
        ${_(u'for real-time arrival information and any Service Alerts that may affect your trip.')}
        %if not is_mobile:
        ${_(u'Call 503-238-RIDE (7433), visit m.trimet.org, or text your Stop ID to 27299.')}
        %endif
    </small></p>

</%def>

##
##
##
<%def name="render_alerts(itinerary)">
    %if itinerary['has_alerts']:
    <div class="box">
        %for alert in itinerary['alerts']:
        ## TODO issue #5599
        ## ${util.alert_content(alert)}
        ${plan_alert_content(alert)}
        %endfor
    </div><!-- end #alerts -->
    %endif
</%def>

<%def name="plan_alert_content(alert)">
    <p><img src="${util.url_domain()}/global/img/icon-alert.png" width="12" />
        <small>${alert['text']} <span class="alert-time">${_(u'As of')} ${alert['start_date_pretty']} <a href="${alert['url']}" target="#">${_(u'(more...)')}</a></span></small>
    </p>
</%def>

<%def name="render_fares(itinerary, fares_url)">
%if has_fare(itinerary):
<p class="fare">${_(u'Fare for this trip')}: <a href="${fares_url}">${_(u'Adult')}: ${itinerary['fare']['adult']}, ${_(u'Youth')}: ${itinerary['fare']['youth']}, ${_(u'Honored Citizen')}: ${itinerary['fare']['honored']}</a></p>
%endif
</%def>

<%def name="pretty_distance(dist)">
<%
    try:
        return str(dist['distance']) + " " + _(dist['measure'])
    except:
        return dist
%>
</%def>

<%def name="get_mode_img(mode)"><%
    ''' return 20x20px mode gif for leg list 
    '''
    ret_val = ''
    path = util.planner_img_url()
    if mode == util.attr.BUS:
        ret_val = path + "/bus.png"
    if mode == util.attr.BICYCLE:
        ret_val = path + "/bicycle.png"
    if mode == util.attr.WALK:
        ret_val =  path + "/walk.png"
    if mode == util.attr.RAIL:
        ret_val = path + "/rail.png"
    if mode == util.attr.TRAM:
        ret_val = path + "/tram.png"
    if mode == util.attr.GONDOLA:
        ret_val = path + "/gondola.png"

    return ret_val
%></%def>

<%def name="get_mode_css_class(mode)"><%
    ''' return css class names
    '''
    ret_val = ''
    if mode == util.attr.BUS:
        ret_val = 'fa-bus'
    if mode == util.attr.CAR:
        ret_val = 'fa-car'
    if mode == util.attr.BICYCLE:
        ret_val = 'fa-bike'
    if mode == util.attr.WALK:
        ret_val = 'fa-walk'
    if mode == util.attr.RAIL:
        ret_val = 'fa-wes'
    if mode == util.attr.TRAM:
        ret_val = 'fa-max'
    if mode == util.attr.GONDOLA:
        ret_val = 'fa-aerialtram'

    return ret_val
%></%def>

##
##
##
<%def name="itin_tab(itin_list, i, text, extra_params='')">
    %if len(itin_list) > i:
        <%
            it  = itin_list[i]
            sel = it['selected']
            n   = it['transfers']
            dur = it['date_info']['duration_min']
            tfer = _('${number} transfer', '${number} transfers', mapping={'number':n})
            fare = it['fare']['adult']
            url  = it['url']
            if n < 0:
                tfer = ''
                fare = _('walk only')
        %>
        <!-- ${_('transfer')} or ${_('transfers')} -->
        %if sel:
        <li class="selected"><span>${text}<br /><small>${dur} ${_('mins')}, ${tfer}<!-- ${fare}--></small></span></li>
        %else:
        <li><a href="${url}${extra_params}">${text}<br /><small>${dur} ${_('mins')}, ${tfer}<!-- ${fare}--></small></a></li>
        %endif
    %endif
</%def>

##
##
##
<%def name="get_optimize(optimize)">
<%
    if optimize == 'SAFE':
        ret_val = _(u'Safest trip')
    elif optimize == 'TRANSFERS':
        ret_val = _(u'Fewest transfers')
    else:
        ret_val = _(u'Quickest trip')
    return ret_val
%>
</%def>

##
## footer of the trip planner form
## a img bar for the imap, with link to the map
##
<%def name="bottom_imap_bar()">
    <div id="imap-wrap">
        <section id="imap" class="group">
            <h3><a href="http://ride.trimet.org" onClick="_gaq.push(['_trackEvent', 'TripPlanner', 'InteractiveMapLink', 'Text planner form link']);"><strong>${_(u'Interactive Map Trip Planner')}</strong> &raquo;</a></h3>
        </section><!-- end #imap -->
    </div><!-- end #promobar-wrap -->
</%def>

##
## footer with the trip plan disclaimer
##
<%def name="bottom_disclaimer(is_mobile=False)">
   ## moved in with the console
</%def>

<%def name="set_planner_text_cookie()">
<script>
try
{
    /** triplanner text cookie ... tripplanner can be used to set / unset form elements, like map button */
    function setCookie(k, v) {
        // want domain to be '.trimet.org'
        // so try to strip off any subdomain
        var dm = document.domain;
        if(dm.indexOf('.') != dm.lastIndexOf('.'))
            dm = dm.substring(dm.indexOf('.'));
        else
            dm = "." + dm
        var domain  = "domain="  + dm;

        var dt = new Date();
        dt.setTime(dt.getTime() + (365*24*60*60*1000));
        var expires = "expires=" + dt.toGMTString();

        document.cookie = k + "=" + v + "; " + expires + "; " + domain + "; path=/;";
    }
    setCookie('tripplanner', 'text');
} catch(e) {}
</script>
</%def>

<%def name="get_depart_arrive(is_arrive_by=False)">
<%
    if is_arrive_by:
        ret_val = _(u'Arrive by')
    else:
        ret_val = _(u'Depart after') 
    return ret_val
%>
</%def>
<%def name="get_depart_arrive_at(is_arrive_by=False)">
<%
    if is_arrive_by:
        ret_val = _(u'Arrive at')
    else:
        ret_val = _(u'Depart at') 
    return ret_val
%>
</%def>

<%def name="get_grade(elev)">${elev['up'] if elev['up'] > elev['down'] else elev['down']}%</%def>
<%def name="check_grade(elev)"><% False if elev is None or (elev['up'] == 0 and elev['down'] == 0) else True %></%def>

<%def name="get_route_name(route)"><% return route['name'] + " " + _(u'to') + " " + route['headsign'] if route['headsign'] else ''%></%def>
<%def name="get_time(itinerary, is_arrive_by)"><% from ott.utils import transit_utils; return transit_utils.get_time(itinerary, is_arrive_by)%></%def>

<%def name="get_itinerary(plan)"><%
    from ott.utils import transit_utils
    ret_val = None
    try:
        ret_val = transit_utils.get_itinerary(plan)
    except:
        pass
    return ret_val
%></%def>
<%def name="has_transit(itinerary)"><% from ott.utils import transit_utils; return transit_utils.has_transit(itinerary)%></%def>
<%def name="has_fare(itinerary)"><% from ott.utils import transit_utils; return transit_utils.has_fare(itinerary)%></%def>
<%def name="get_route_link(name, url, mode)"><a href="${url}" title="${_(u'Show route map and schedules for this line')}" class="step-mode"><i class="${get_mode_css_class(mode)}"></i> ${name}</a></%def>
<%def name="get_interline_note(interline)">
%if interline != None:
${_(u'which continues as ')} ${interline} (${_(u'stay on board')})
%endif
</%def>

<%def name="render_elevation(elevation, no_expand=False)">
            %if elevation != None:
                <p class="elevation"><span>
                    ${_(u'Elevation gain')}: ${_(u'${number} foot', u'${number} feet', mapping={'number':elevation['rise_ft']})}<br/>
                    ${_(u'Elevation loss')}: ${_(u'${number} foot', u'${number} feet', mapping={'number':elevation['fall_ft']})}<br/>
                    %if check_grade(elevation['grade']):
                    ${_(u'Steepest grade')}: ${get_grade(elevation['grade'])}<br/>
                    %endif
                    %if elevation['points'] and len(elevation['points']) > 2:
                    <span class="elevation_txt">${_(u'Elevation chart')}</span><span class="elevation_chart">${util.dynamic_img("sparkline?points=" + elevation['points'], 100, 20, no_expand=no_expand)}</span>
                    %endif
                    </span>
                </p>
            %endif
</%def>

<%def name="render_start_end_maps(from_img_url, to_img_url, no_expand=False)">
        <div class="maps">
             <p class="walk-start">${_(u'Start')}<br />${util.dynamic_img(from_img_url, 300, 288, _(u'Map of starting point (300x288)'), no_expand=no_expand)}</p>
             <p class="walk-end">${_(u'End')}<br/>${util.dynamic_img(to_img_url, 300, 288, _(u'Map of ending point (300x288)'), no_expand=no_expand)}</p>
        </div><!-- end maps -->
</%def>


## They want 2-stage walk instructions, as per mock up...
## https://github.com/OpenTransitTools/view/blob/a5e80acff83277e593fb09b760ce94cf7311b454/ott/view/templates/desktop/planner.html
## <img src="images/directions/right.png"/>
<%def name="render_steps(verb, frm, to, steps)">
    <ol>
        %for i, s in enumerate(steps):
        <%
            name = s['name']
            preposition = _(u'on')
            if i == 0:
                preposition = _(u'from')

            if name and name.lower() == 'elevator':
                continue

            # find default names when name info does not exist (common for first/last step) 
            if name == None or name == '':
                # first step, name == from place
                if i == 0:
                    name = frm
                    preposition = _(u'from')
                # last step, name == to place
                elif i+1 == len(steps):
                    name = to
                    preposition = _(u'to')
                # if we have no name, then do what???
                else:
                    name = ''

            instruct_verb = verb
            turn = None
            dir = s['relative_direction']
            if dir != None:
                dir = dir.lower().replace('_', ' ').strip()
                if dir == ('elevator'):
                    turn = _(u'Take the elevator to level ') + name
                    instruct_verb = None
                elif dir not in ('continue'):
                    turn = _(u'Turn') + " " + _(dir) + " " + _(u'on') + " " + _(name)
                else:
                    instruct_verb = dir.title()
            if instruct_verb:
                instruct = _(instruct_verb) + " " + pretty_distance(s['distance']) + " " + _(s['compass_direction']) + " " + preposition + " " + _(name)
            else:
                instruct = None
        %>
        %if turn != None:
        <li>${turn}</li>
        %endif
        %if instruct != None:
        <li>${instruct}</li>
        %endif
        %endfor
    </ol>
</%def>


<%def name="render_bicycle_leg(leg, i, extra_params='', no_expand=False)">
    <li>
        <div class="step-number"><span>${i}</span></div>
        <p class="directions">
            <%
                dir = leg['compass_direction'] if leg['compass_direction'] else ''
                bike_title = _(u'Bike') + " " + _(dir) + " " + pretty_distance(leg['distance'])
            %>
            ${bike_title} ${_(u'to')}
            %if leg['to']['stop']:
            <a href="${leg['to']['stop']['info']}${extra_params}" title="${_(u'Show more information about this stop/station')}">${leg['to']['name']}</a>
            %else:
            ${leg['to']['name']}
            %endif

            %if leg['to']['stop']:
            <span class="stopid">${_(u'Stop ID')}&nbsp;${leg['to']['stop']['id']}</span>
            %endif
        </p>

        <div class="normal"><!-- hidden biking directions and map -->
            <a href="#leg_${i}" onClick="expandMe(this);" class="open"><span class="open-text" title="${_(u'Show biking directions')}">${_(u'Details')}</span><span class="close-text">${_(u'Close')}</span></a>
            <div class="description">
                ${render_elevation(leg['elevation'], no_expand)}
                ${render_steps(_(u'Bike'), leg['from']['name'], leg['to']['name'], leg['steps'])}
                ${render_start_end_maps(leg['from']['map_img'], leg['to']['map_img'], no_expand=no_expand)}
                    <!--
                    TODO TODO TODO
                    1. generic 'direction' element in json
                    2. enum for different walk insturctions Straight/Left/Slight Left/etc...
                    3. Reformat entire Leg, ala what happens on old trip planner...
                       http://maps5.trimet.org/maps/print/V1/tripplanner?fromPlace=pdx&toPlace=zoo&time=6:45%20pm
                    4. Dynamic Load Images... 
                    TODO TODO TODO
                    -->
            </div><!-- end .description -->
        </div><!-- end .normal/hidden walking directions -->
    </li>
</%def>

<%def name="render_walk_leg(leg, i, extra_params='', no_expand=False)">
    <li>
        <div class="step-number"><span>${i}</span></div>
        <p class="directions">
            <% 
                walk_title = _(u'Walk') + " " + pretty_distance(leg['distance'])
            %>
            %if leg['steps']:
                ${walk_title} ${_(u'to')}
            %elif leg['to']['stop'] and leg['transfer']:
                ${_(u'Go to')}
            %else:
                ${walk_title} ${_(u'to')}
            %endif
            %if leg['to']['stop']:
                <a href="${leg['to']['stop']['info']}${extra_params}" title="${_(u'Show more information about this stop/station')}">${leg['to']['name']}</a>
            %else:
                ${leg['to']['name']}
            %endif
            %if leg['to']['stop']:
                <span class="stopid">${_(u'Stop ID')}&nbsp;${leg['to']['stop']['id']}</span>
            %endif
        </p>

        <div class="normal"><!-- hidden walking directions and map -->
            %if no_expand:
            <div class="description">
            %else:
            <a href="#leg_${i}" onClick="expandMe(this);" class="open"><span class="open-text" title="${_(u'Show walking directions')}">${_(u'Details')}</span><span class="close-text">${_(u'Close')}</span></a>
            <div class="description">
            %endif
            %if leg['steps']:
                ${render_elevation(leg['elevation'], no_expand)}
                ${render_steps(_(u'Walk'), leg['from']['name'], leg['to']['name'], leg['steps'])}
                ${render_start_end_maps(leg['from']['map_img'], leg['to']['map_img'], no_expand=no_expand)}
            %endif
            </div><!-- end .description -->
        </div><!-- end .normal/hidden walking directions -->
    </li>
</%def>

<%def name="is_interline(leg_list, n)">
<%
    ret_val = False
    try:
        if leg_list[n]['interline']:
            ret_val = True
    except:
        pass
    return ret_val
%>
</%def>

##
## Stop Leg is artificially created leg in order to show links to the stop
## Used when the first leg of the itin is a transit leg...
##
<%def name="render_stop_leg(leg, i, extra_params='')">
    <li>
        <div class="step-number"><span>${i}</span></div>
        <p class="directions">
            ${_(u'Go to')}
            <a href="${leg['from']['stop']['info']}${extra_params}" title="${_(u'Show more information about this stop/station')}">${leg['from']['name']}</a>
            <span class="stopid">${_(u'Stop ID')}&nbsp;${leg['from']['stop']['id']}</span>
        </p>
        <div class="normal">
            <div class="description"></div><!-- end .description -->
        </div><!-- end .normal/hidden walking directions -->
    </li>
</%def>

##
## Meat of the transit narrative...
##
<%def name="render_transit_leg(leg_list, n, i, j, is_mobile, extra_params='')">
    <li>
        <div class="step-number"><span>${i}</span></div>
        <p class="directions">
            <%
                leg = leg_list[n] 

                route_name = get_route_name(leg['route'])
                route_mode = leg['mode']

                from_sched = leg['from']['stop']['schedule']
                from_name  = leg['from']['name']
                from_stop  = leg['from']['stop']['id']
                start_time = leg['date_info']['start_time']

                # with interline trips, we use the next leg for the arrival time / stop / etc...
                # (interline leg itself will be skipped ... see logic in render_leg(), which 'pass'es on interlines )
                interline = None
                if is_interline(leg_list, n+1):
                    leg = leg_list[n+1]
                    interline = leg['route']['name']

                to_sched   = leg['to']['stop']['schedule']
                to_name    = leg['to']['name']
                to_stop    = leg['to']['stop']['id']
                end_time   = leg['date_info']['end_time']

                if is_mobile:
                    route_url = leg['route']['schedulemap_url']
                else:
                    route_url = leg['route']['url']
            %>
            <a href="${from_sched}${extra_params}" title="${_(u'Show schedule for')} ${from_name}" class="step-time"><span>${start_time}</span></a> ${_(u'Board')} ${get_route_link(route_name, route_url, route_mode)}${get_interline_note(interline)}
            %if leg['alerts']:
            <a href="#alerts" title="${_(u'A Service Alert is in effect that may affect this trip. Click for details.')}" class="step-alert"><img src="${util.url_domain()}/global/img/icon-alert.png" width="12" /></a>
            %endif
        </p>
    </li>

    <li>
        <div class="step-number"><span>${j}</span></div>
        <p><a href="${to_sched}${extra_params}" title="${_(u'Show schedule for')} ${to_name}" class="step-time"><span>${end_time}</span></a> ${_(u'Get off at')} <a href="${leg['to']['stop']['info']}${extra_params}" title="${_(u'Show more information about this stop')}">${to_name}</a> <span class="stopid">${_(u'Stop ID')}&nbsp;${to_stop}</span></p>
    </li>
</%def>

<% leg_id = 1 %>
<%def name="_render_leg(itinerary, n, is_mobile, extra_params, no_expand)">
<%
    ''' call render stuff above...
    '''
    ret_val = ''

    global leg_id
    if n == 0:
        leg_id = 1

    leg_list = itinerary['legs']
    leg = leg_list[n]

    if is_interline(leg_list, n):
        pass   # ignore interline legs (assume they're interline transit legs, which are handled below)
    elif leg['mode'] in util.attr.TRANSIT_MODES:
        ## when the first leg is transit, show a go-to stop leg, so that we have a link to the stop...
        if n == 0:
            render_stop_leg(leg_list[n], leg_id, extra_params)
            leg_id = leg_id + 1
        ret_val = render_transit_leg(leg_list, n, leg_id, leg_id+1, is_mobile, extra_params)
        leg_id = leg_id + 2 
    elif leg['mode'] == util.attr.WALK:
        ret_val = render_walk_leg(leg, leg_id, extra_params, no_expand)
        leg_id = leg_id + 1 
    elif leg['mode'] == util.attr.BICYCLE:
        ret_val = render_bicycle_leg(leg, leg_id, extra_params, no_expand)
        leg_id = leg_id + 1

    return ret_val
%>
</%def>
