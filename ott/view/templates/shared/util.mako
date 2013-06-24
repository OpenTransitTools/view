## -*- coding: utf-8 -*-
<%def name="url_domain()"><%return "http://dev.trimet.org"%></%def>
<%def name="img_url()">${url_domain()}/images/triptools</%def>
<%def name="planner_img_url()">${img_url()}/mode</%def>

<%!
    ''' access these variables in other space via <namespace>.attr, ala util.attr, ala util.attr.WALK
    '''
    WALK       = 'WALK'
    BICYCLE    = 'BICYCLE'
    TRAM       = 'TRAM'
    SUBWAY     = 'SUBWAY'
    STREETCAR  = 'STREETCAR'
    RAIL       = 'RAIL'
    BUS        = 'BUS' 
    CAR        = 'CAR' 
    CABLE_CAR  = 'CABLE_CAR' 
    GONDOLA    = 'GONDOLA'
    FERRY      = 'FERRY'
    FUNICULAR  = 'FUNICULAR'
    TRANSIT    = 'TRANSIT'
    TRAINISH   = 'TRAINISH' 
    BUSISH     = 'BUSISH'
    TRAIN      = 'TRAIN' 
%>

## misc methods (defined someplace in the shared space...needed for things to work.
<%def name="form(url='', method='get', class_='form-style')"></%def>
<%def name="end_form()"></%def>
<%def name="select(name='route', stuff=[], options='')"></%def>
<%def name="route_select_options()"></%def>
<%def name="url_for(controller='main', action='route_stops_list')"></%def>


<%def name="month_options(selected)">
    %for m in (_(u'January'), _(u'February'), _(u'March'), _(u'April'), _(u'May'), _(u'June'), _(u'July'), _(u'August'), _(u'September'), _(u'October'), _(u'November'), _(u'December')):
        <option value="${loop.index + 1}" ${'selected' if m == selected or str(loop.index+1) == str(selected) else ''} >${m}</option>
    %endfor
</%def>
<%def name="month_select(selected)"><select name="month" tabindex="7" >
    ${month_options(selected)}
    </select></%def>


<%def name="month_abbv_options(selected)">
    %for m in (_(u'Jan'), _(u'Feb'), _(u'Mar'), _(u'Apr'), _(u'May'), _(u'Jun'), _(u'Jul'), _(u'Aug'), _(u'Sep'), _(u'Oct'), _(u'Nov'), _(u'Dec')):
        <option value="${loop.index + 1}" ${'selected' if  m == selected or str(loop.index+1) == str(selected) else ''}>${m}</option>
    %endfor
</%def>
<%def name="month_abbv_select(selected)"><select name="month" tabindex="7" >
    ${month_abbv_options(selected)}
    </select></%def>


<%def name="day_options(selected)">
    %for d in range(1, 32):
        <option value="${d}" ${'selected' if d == selected else ''}>${d}</option>
    %endfor
</%def>
<%def name="day_select(selected=1)"><select name="day" tabindex="8" >
    ${day_options(selected)}
    </select></%def>

<%def name="link_or_strong(label, make_strong, url, label_prefix='', l_bracket='[', r_bracket=']')">
    %if make_strong:
        <strong>${label}</strong>
    %else:
        <a href="${url}"><!--${label_prefix}--> ${label}</a>
    %endif
</%def>

<%def name="alerts_inline_icon_link(img_url='/images/triptools/alert-icon.png')">
    <!--<a href="#alerts" class="alert"><img border="0" src="${url_domain()}${img_url}" alt="${_(u'See footnote')}" title="${_(u'See footnote')}"/></a>-->
	<a href="#alerts" class="stop-alert"><img src="${url_domain()}${img_url}" alt="Service alert at this stop" /></a>
</%def>

<%def name="alerts(alert_list, img_url='/images/triptools/alert.png')">
    <div id="alerts" class="group">
        <!--<h3><a href="${url_domain()}/alerts/">${_(u'Service Alerts')}</a></h3>-->
        %for a in alert_list:
            <p><img src="${url_domain()}${img_url}" />
                <span class="alert-text"><b>${a['name']}</b><br />${a['description']}</span>
                <span class="alert-time">TODO ??? As of March 19 @ 10:15am ??? TODO</span>
            </p>
        %endfor
    </div>
</%def>
