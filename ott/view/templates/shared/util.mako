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
<%def name="option(v, p, selected=False)"><option ${'selected="selected"' if selected else '' | n} value="${v}">${p}</option></%def>

<%def name="stop_and_city_name(stop)">
<%
    ret_val = stop['name']
    if city in stop and len(stop['city']) > 1 and stop['city'] != Null and stop['city'] != "Null":
         ret_val = "{0} {1} {2}".format(stop['stop'], _(u'in'), stop['city'])
    return ret_val
%>
</%def>

<%def name="get_locale(def_val='en')">
<%
    from ott.view.utils import html_utils
    ret_val = def_val
    try:
        loc = html_utils.get_first_param(request, '_LOCALE_')
        if loc:
            ret_val = loc
        
    except:
        ret_val = def_val
    return ret_val
%>
</%def>


<%def name="get_extra_params(def_val='')">
<%
    ''' extra_params: this variable is built here, and should be appended to all <a href> urls.  The string is pre-pended with
        an ampersand, so if there are no parameters on a given url, maybe add something bogus to the url prior to ${extra_parmas}
    '''
    extra_params=def_val

    # step 1: append any locale url param to extra_params... 
    loc = get_locale(None)
    if loc:
        extra_params = "{0}&_LOCALE_={1}".format(extra_params, loc)

    return extra_params
%>
</%def>

<%def name="get_extra_params_hidden_inputs()">
<%
    loc = get_locale(None)
%>
    %if loc:
        <input type="hidden" name="_LOCALE_" value="${loc}"/>
    %endif
</%def>


<%def name="form_help_right()">
                    <div class="form-help-popup-onright">
                        <p>
                            ${_(u'There are several ways to enter a location')}:<br/>
                            <b>${_(u'Address')}</b><br /><kbd>4012 SE 17</kbd><br />
                            <b>${_(u'Intersection')}</b> ${_(u'(where two streets cross each other)')}<br /><kbd>SE 17 &amp; Center</kbd>.<br />
                            <b>${_(u'Landmarks')}</b><br /><kbd>PDX</kbd><br /><kbd>Rose Quarter Arena</kbd><br /><kbd>Clackamas Town Center</kbd>.
                        </p>
                    </div>
</%def>

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

<%def name="compare_values(a, b)">
<%
    ret_val = False
    try:
        ret_val = float(a) == float(b)
    except:
        ret_val = a == b
    return ret_val
%>
</%def>


