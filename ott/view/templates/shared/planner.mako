##
## 
##
<%namespace name="util"  file="/shared/util.mako"/>

<%def name="get_mode_img(mode)">
<%
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
%>
</%def>

<%def name="get_mode_css_class(mode)">
<%
    ''' return css class names
    '''
    ret_val = ''
    if mode == util.attr.BUS:
        ret_val = 'step-bus-icon'
    if mode == util.attr.CAR:
        ret_val = 'step-car-icon'
    if mode == util.attr.BICYCLE:
        ret_val = 'step-bike-icon'
    if mode == util.attr.WALK:
        ret_val = 'step-walk-icon'
    if mode == util.attr.RAIL:
        ret_val = 'step-wes-icon'
    if mode == util.attr.TRAM:
        ret_val = 'step-max-icon'
    if mode == util.attr.GONDOLA:
        ret_val = 'step-aerialtram-icon'

    return ret_val
%>
</%def>

<%def name="itin_tab(itin_list, i, text)">
    %if len(itin_list) > i:
        <%
            it  = itin_list[i]
            sel = it['selected']
            n   = it['transfers']
            dur = it['date_info']['duration_min']
            tfer = _('transfer', 'transfers', mapping={'number':n})
            fare = it['fare']['adult']
            url  = it['url']
        %>
        <!-- ${_('transfer')} or ${_('transfers')} -->
        %if sel:
        <li class="selected"><span><b>${text}</b><br />${dur} ${_('mins')}, ${tfer}, ${fare}</span></li>
        %else:
        <li class="normal"><a href="${url}"><span><b>${text}</b><br/>${dur} ${_('mins')}, ${tfer}, ${fare}</span></a></li>
        %endif
    %endif
</%def>

<%def name="get_optimize(plan)">
<%
    if plan['optimize'] == 'SAFE':
        optimize = _(u'Safest trip')
    elif plan['optimize'] == 'TRANSFERS':
        optimize = _(u'Fewest transfers')
    else:
        optimize = _(u'Quickest trip')
    return optimize
%>
</%def>

<%def name="get_time(plan, itinerary)">
<%
    if plan['arrive_by']:
        time = itinerary['date_info']['end_time']
    else:
        time = itinerary['date_info']['start_time']
    return time
%>
</%def>

<%def name="get_itinerary(plan)">
<%
    # find target itinerary 
    for itin in plan['itineraries']:
        itinerary = itin
        if itin['selected']:
            break
    return itinerary
%>
</%def>

<%def name="get_depart_arrive(plan)">
<%
    if plan['arrive_by']:
        depart_arrive = _(u'Arrive by')
    else:
        depart_arrive = _(u'Depart after') 
    return depart_arrive
%>
</%def>


<%def name="get_route_name(route)">${route['name']}${' ' + _(u'to') + ' ' + route['headsign'] if route['headsign'] else ''}</%def>
<%def name="get_route_link(route, mode)">
%if route is not None:
<a href="${route['url']}" target="#" title="${_(u'Show map and schedules for this route.')}" class="step-mode"><img src="${util.img_url()}/modes.png" width="0" height="1" class="${get_mode_css_class(mode)}" />${get_route_name(route)}</a>
%else:
${_(u'transit vehicle')}
%endif
</%def>

<%def name="render_elevation(up, down, grade)">
                <p class="elevation"><span>
                    ${_(u'Total elevation uphill')}: ${_(u'${number} foot', u'${number} feet', mapping={'number':up})}<br />
                    ${_(u'Total elevation downhill')}: ${_(u'${number} foot', u'${number} feet', mapping={'number':down})}<br />
                    ${_(u'Steepest grade')}: ${grade}<br />
                    <a href="#">${_(u'Elevation chart')}</a></span>
                </p>
</%def>

<%def name="render_start_end_maps(from_img_url, to_img_url)">
                <div class="maps">
                    <p class="walk-start">${_(u'Start')}<br /><img src="${from_img_url}" alt="${_(u'Map of starting point (300x288)')}" width="300" height="288" /></p>
                    <p class="walk-end">
                        ${_(u'End')}
                        <br />
                        <img src="${to_img_url}" alt="${_(u'Map of ending point (300x288)')}" width="300" height="288" />
                    </p>
                </div><!-- end .maps -->
</%def>

<%def name="render_steps(steps)">
                <ol>
                    %for l in steps:
                    <li>${l['name']}</li>
                    %endfor
                </ol>
</%def>

<%def name="render_bicycle_leg(leg, i)">
    <li class="num${i}">
        <div class="step-number"><img src="${util.img_url()}/numbers.png" width="0" height="1" /></div>
        <p>
            <%
                dir = leg['compass_direction'] if leg['compass_direction'] else ''
                bike_title = "{0} {1} {2}".format(_(u'Bike'), dir, leg['distance'])
            %>
            ${bike_title} ${_(u'to')}
            %if leg['to']['stop']:
            <a href="${leg['to']['stop']['info']}" title="${_(u'Click for more information about this stop')}">${leg['to']['name']}</a>
            %else:
            ${leg['to']['name']}
            %endif

            %if leg['to']['stop']:
            <span class="stopid">${_(u'Stop ID')}&nbsp;${leg['to']['stop']['id']}</span>
            %endif
        </p>

        <div class="normal"><!-- hidden walking directions and map -->
            <a href="#leg_${i}" onClick="expandMe(this);" title="${_(u'Biking directions')}" class="open"><span>${_(u'Biking directions')}</span></a>
            <div class="description">
                ${render_elevation(7, 1, '4%')}
                ${render_steps(leg['steps'])}
                ${render_start_end_maps(leg['from']['map_img'], leg['to']['map_img'])}
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

<%def name="render_walk_leg(leg, i)">
    <li class="num${i}">
        <div class="step-number"><img src="${util.img_url()}/numbers.png" width="0" height="1" /></div>
        <p>
            <% 
                dir = leg['compass_direction'] if leg['compass_direction'] else ''
                walk_title = "{0} {1} {2}".format(_(u'Walk'), dir, leg['distance'])
            %>
            %if leg['steps']:
            ${walk_title} ${_(u'to')}
            %elif leg['to']['stop'] and leg['transfer']:
            ${_(u'Go to')}
            %else:
            ${walk_title} ${_(u'to')}
            %endif
            %if leg['to']['stop']:
            <a href="${leg['to']['stop']['info']}" title="${_(u'Click for more information about this stop')}">${leg['to']['name']}</a>
            %else:
            ${leg['to']['name']}
            %endif
            %if leg['to']['stop']:
            <span class="stopid">${_(u'Stop ID')}&nbsp;${leg['to']['stop']['id']}</span>
            %endif
        </p>

        <div class="normal"><!-- hidden walking directions and map -->
            <a href="#leg_${i}" onClick="expandMe(this);" title="${_(u'Walking directions')}" class="open"><span>${_(u'Walking directions')}</span></a>
            <div class="description">
                %if leg['steps']:
                ${render_elevation(7, 1, '4%')}
                ${render_steps(leg['steps'])}
                ${render_start_end_maps(leg['from']['map_img'], leg['to']['map_img'])}
                %endif
            </div><!-- end .description -->
        </div><!-- end .normal/hidden walking directions -->
    </li>
</%def>

<%def name="render_transit_leg(leg, i, j)">
    <li class="num${i}">
        <div class="step-number"><img src="${util.img_url()}/numbers.png" width="0" height="1" /></div>
        <p>
            <a href="${leg['from']['stop']['schedule']}" title="${_(u'Show schedule for')} ${leg['from']['name']}" class="step-time">${leg['date_info']['start_time']}</a> ${_(u'Board')} ${get_route_link(leg['route'], leg['mode'])} 
            %if leg['alerts']:
            <a href="#alerts" title="${_(u'There is an alert that applies to this transit leg.  See the "alerts" section below for details')}" class="step-alert"><img src="${util.img_url()}/alert.png" /></a>
            %endif
        </p>
    </li>

    <li class="num${j}">
        <div class="step-number"><img src="${util.img_url()}/numbers.png" width="0" height="1" /></div>
        <p><a href="${leg['to']['stop']['schedule']}" title="${_(u'Show schedule for')} ${leg['to']['name']}" class="step-time">${leg['date_info']['end_time']}</a> ${_(u'Get off at')} <a href="${leg['to']['stop']['info']}" title="${_(u'More information about this stop')}">${leg['to']['name']}</a> <span class="stopid">${_(u'Stop ID')}&nbsp;${leg['to']['stop']['id']}</span></p>
    </li>
</%def>

<% leg_id = 1 %>
<%def name="render_leg(leg, n)">
<%
    ''' call render stuff above...
    '''
    ret_val = ''

    global leg_id
    if n == 0:
        leg_id = 1
    if leg['mode'] in (util.attr.BUS, util.attr.TRAM, util.attr.RAIL, util.attr.TRAIN, util.attr.GONDOLA):
        ret_val = render_transit_leg(leg, leg_id, leg_id+1)
        leg_id = leg_id + 2 
    elif leg['mode'] == util.attr.WALK:
        ret_val = render_walk_leg(leg, leg_id)
        leg_id = leg_id + 1 
    elif leg['mode'] == util.attr.BICYCLE:
        ret_val = render_bicycle_leg(leg, leg_id)
        leg_id = leg_id + 1

    return ret_val
%>
</%def>
