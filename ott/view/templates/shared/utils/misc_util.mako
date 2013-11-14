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

<%def name="get_ele(struct, name, def_val=None)">
<%
    ret_val = def_val
    if name in struct and struct[name]:
        ret_val = struct[name]
    return ret_val
%>
</%def>


<%def name="localize_str(s, def_val=None)">
<%
    ret_val = def_val
    try:
        if s is not None:
            ret_val = _(s)
            if len(s) < 1:
                ret_val = def_val
    except:
        ret_val = def_val
    return ret_val
%>
</%def>

<%def name="unicode_to_str(s, def_val=None)">
<%
    ret_val = def_val
    try:
        if s:
            ret_val = str(s)
    except:
        ret_val = def_val
    return ret_val
%>
</%def>

<%def name="name_city_str(name, city, type_name=None, stop_id='')">
<%
    ret_val = _(u'Undefined')
    if name and len(name) > 0:
        ret_val = name.replace('%26', '&')

    city = localize_str(city)
    tn = localize_str(type_name, type_name)
    type_name = unicode_to_str(tn, type_name) # have to do this for .format()
    if stop_id is None:
        stop_id = ''

    try:
        if city and type_name:
            ret_val = "{0} ({1} {2} {3} {4})".format(ret_val, type_name, stop_id, _(u'in'), city)
        elif city:
            ret_val = "{0} ({1} {2})".format(ret_val, _(u'in'), city)
        elif type_name and len(stop_id) > 0:
            ret_val = "{0} ({1} {2})".format(ret_val, type_name, stop_id)
        elif type_name:
            ret_val = "{0} ({1})".format(ret_val, type_name)
    except:
        pass


    return ret_val
%>
</%def>


<%def name="name_city_str_from_struct(struct)">
<%
    name = get_ele(struct, 'name')
    city = get_ele(struct, 'city')
    name_city = name_city_str(name, city) 
    return name_city
%>
</%def>

## ...
<%def name="map_place_link(place, path_prefix='')">
<%
    extra_params = get_extra_params()
    name = get_ele(place, 'name', _(u'Undefined'))
    city = get_ele(place, 'city', '')
    name_city = name_city_str_from_struct(place)
%>
<a href="${path_prefix}map_place.html?name=${name}&city=${city}&lon=${place['lon']}&lat=${place['lat']}${extra_params}">${name_city}</a>
</%def>

## from / to links
<%def name="plan_a_trip_links(name, lon, lat, extra_params='')">
<!-- TODO: fix these urls, so that urls are dynamic / off depending upon agency, etc... -->
<h3 class="tight">${_(u'Plan a trip')}</h3>
<p>
  <a href="planner_form.html?to=${name}::${lat},${lon}${extra_params}"
    title="${_(u'Plan a trip')} ${_(u'to')} ${name}"
    >${_(u'To here')}</a> &nbsp;&bull;&nbsp; <a 
    href="planner_form.html?from=${name}::${lat},${lon}${extra_params}"
    title="${_(u'Plan a trip')} ${_(u'from')} ${name}"
    >${_(u'From here')}</a>
</p>
</%def>

## dynamic img ... see dynamiclyLoadImages() in triptools.js for more
<%def name="dynamic_img(url, w, h, alt='dynamic img (requires javascript)', def_img='http://maps.trimet.org/images/ui/s.gif')"><img dsrc="${url}" dwidth="${w}" dheight="${h}" alt="${alt}" src="${def_img}"/></%def>

<%def name="has_url_param(param_name)">
<%
    from ott.view.utils import html_utils
    ret_val = False
    loc = html_utils.get_first_param(request, param_name)
    if loc:
        ret_val = True
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


<%def name="print_year()"><%
    from ott.view.utils import date_utils
    dt = date_utils.get_day_info()
%>${dt['year']}</%def>


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


