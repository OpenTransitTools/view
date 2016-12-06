## -*- coding: utf-8 -*-

<%def name="get_ini_param(name, def_val=None)"><%
    ret_val = def_val
    try:
        ret_val = request.registry.settings[name]
        ret_val.strip()
    except Exception, e:
        #print e
        pass
    return ret_val
%></%def>

<%def name="url_domain()"><% return get_ini_param('ott.css_url', '') %></%def>
<%def name="is_test()"><% return get_ini_param('ott.is_test') %></%def>

<%def name="error_msg(extra_params, feedback_url)">
<%
    error_message = get_first_param('error_message')
    app_name      = get_first_param('app_name', 'Trip Planner')
%>
%if error_message and error_message != 'None':
<h2 class="error">${_(error_message)}</h2>
%else:
<h2 class="error">${_(u'The')} ${_(app_name)} ${_(u'is not working...')}</h2>
%endif
<p align="center"><a href="${feedback_url}">${_(u'Contact us')}</a> ${_(u'let us know more')}.</p>
</%def>

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
    TRANSIT_MODES = (BUS, TRAM, RAIL, TRAIN, GONDOLA, FUNICULAR, FERRY, CABLE_CAR, SUBWAY, STREETCAR, BUSISH, TRAINISH, TRANSIT)
%>

## misc methods (defined someplace in the shared space...needed for things to work.
<%def name="form(url='', method='get', class_='form-style')"></%def>
<%def name="end_form()"></%def>
<%def name="select(name='route', stuff=[], options='')"></%def>
<%def name="route_select_options()"></%def>
<%def name="url_for(controller='main', action='route_stops_list')"></%def>
<%def name="option(v, p, selected=False, show=True)"><option ${'selected="selected"' if selected else '' | n} value="${v}">${p}</option></%def>

<%def name="get_ele(struct, name, def_val=None)"><%
    ret_val = def_val
    if name in struct and struct[name]:
        ret_val = struct[name]
    return ret_val
%></%def>

<%def name="get_val(val, def_val=None)">
<%
    ret_val = def_val
    if val:
        ret_val = val
    return ret_val
%>
</%def>

<%def name="localize_str(s, def_val=None)"><%
    ret_val = def_val
    try:
        if s == "None":
            s = None
        elif s is not None:
            ret_val = _(s)
            if len(s) < 1:
                ret_val = def_val
    except:
        ret_val = def_val
    return ret_val
%></%def>

<%def name="unicode_to_str(s, def_val=None)"><%
    ret_val = def_val
    try:
        if s:
            ret_val = str(s)
    except:
        ret_val = def_val
    return ret_val
%></%def>

<%def name="clean_name(name)"><% return name.replace('%26', '&').replace('%27', "'") %></%def>

<%def name="name_city_stopid(name, city, type=None, id=None)"><%
    ret_val = _(u'Undefined')
    try:
        stop = ''
        if type == 'stop':
            stop = " (" + _(u'Stop ID') + " " + id + ")"
        if city:
            city = ', ' + city
        else:
            city = ''
        ret_val = clean_name(name) + city + stop
    except:
        pass
    return ret_val
%></%def>

<%def name="name_city_str(name, city, type_name=None, stop_id='')"><%
    ret_val = _(u'Undefined')
    if name and len(name) > 0:
        ret_val = clean_name(name)

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
%></%def>

<%def name="name_city_str_from_struct(struct)"><%
    name = get_ele(struct, 'name')
    city = get_ele(struct, 'city')
    name_city = name_city_str(name, city) 
    return name_city
%></%def>

## 
## 
## 
<%def name="map_place_link(place, path_prefix='')"><%
    extra_params = get_extra_params()
    name = get_ele(place, 'name', _(u'Undefined'))
    city = get_ele(place, 'city', '')
    name_city = name_city_str_from_struct(place)
%>${name_city} <a href="${path_prefix}map_place.html?name=${prep_url_params(name, True)}&city=${prep_url_params(city)}&lon=${place['lon']}&lat=${place['lat']}${extra_params}"><small>Map</small></a>
</%def>

<%def name="get_url(url=None)"><%
    ret_val = url
    if url is None:
        host = get_ini_param('ott.host_url', request.host_url)
        ret_val = "{0}{1}".format(host, request.path_qs)
    ret_val = prep_url_params(ret_val, url_escape=True, spell_and=True)
    return ret_val
%></%def>

##
## FEEDBACK URL: http://trimet.org/mailforms/tripfeedback?mailform[subject]=Stop X&mailform[url]=<a href='app url'>Blah</a>
##
## TODO: have a default feedback_url, and override this method for trimet...
## 
<%def name="trimet_feedback_url(subject, message=None, url=None)"><% 
    # default to url in request object 
    if url is None:
        url = get_url(url)
    if message is None:
        message = get_url(url)

    # localized mailform app
    mailform_page="tripfeedback"
    if request.locale_name == 'es':
        mailform_page="es_tripfeedback"

    subject = prep_url_params(subject, url_escape=True, spell_and=True)
    message = prep_url_params(message, url_escape=True, spell_and=True)
%>http://trimet.org/mailforms/${mailform_page}?mailform[subject]=${subject}&mailform[url]=<a href='${url}'>${message}</a></%def>

## TODO: localize???
<%def name="mailto_url(subject='Link to TriMet', message='Check out this page on trimet.org', url=None)"><%
    if url is None:
        url = get_url(url)
    subject = prep_url_params(subject, url_escape=True, spell_and=True)
    message = prep_url_params(message, url_escape=True, spell_and=True)
%>mailto:?subject=${subject}&body=${message}%20:%20${url}</%def>


<%def name="mailto_geocoder(place, svc, url='TripTech@trimet.org')"><%
    subject='Error geocoding an address'
    message='Having trouble finding this address search string'
    subject = prep_url_params(subject, url_escape=True, spell_and=True)
    message = prep_url_params(message, url_escape=True, spell_and=True)

    place   = prep_url_params(place,   url_escape=True, spell_and=True)
    geo = "\n\nhttp://trimet.org/ride/{0}{1}".format(svc, place)
    geo = prep_url_params(geo, url_escape=True, spell_and=True)
%>mailto:${url}?subject=${subject}&body=${message}:%20${place} ${geo}</%def>

<%def name="geocoder_feedback(geo, svc='stop_select_geocode.html?place=')">
<p><small>${_(u"Can’t find your address?")} <a href="${mailto_geocoder(geo, svc)}">${_(u'Please let us know')}</a> ${_(u'so we can improve the Trip Planner')}.</small></p>
</%def>

##
## from / to links
## TODO: fix these urls, so that urls are dynamic / off depending upon agency, etc...\
##
<%def name="plan_a_trip_links(name, lon, lat, extra_params='')">
<h3>${_(u'Plan a trip')}</h3>
<p><a href="/#/planner/form/to=${make_named_coord(name, lat, lon)}${extra_params}" title="${_(u'Plan a trip')} ${_(u'to')} ${name}" class="tripplanner"><i class="fa-tp-outline"></i> ${_(u'To here')}</a></p>
<p><a href="/#/planner/form/from=${make_named_coord(name, lat, lon)}${extra_params}" title="${_(u'Plan a trip')} ${_(u'from')} ${name}" class="tripplanner"><i class="fa-tp-outline"></i> ${_(u'From here')}</a></p>
</%def>

##
## dynamic img ... see dynamiclyLoadImages() in triptools.js for more
##
<%def name="dynamic_img(url, w, h, alt='dynamic img (requires javascript)', def_img='//maps.trimet.org/images/ui/s.gif', no_expand=False)">
%if no_expand:
<img src="${url}" alt="${alt}"/>
%else:
<img dsrc="${url}" dwidth="${w}" dheight="${h}" alt="${alt}" src="${def_img}"/>
%endif
</%def>

<%def name="make_named_coord(name, lat, lon)">
<%
    name = unicode(name)
    name = name.replace('&', '%26')
    ret_val = u"{0}::{1},{2}".format(name, lat, lon)
    return ret_val
%>
</%def>

<%def name="make_named_coord_from_obj(obj)">
<%
    return make_named_coord(obj['name'], obj['lat'] ,obj['lon']) 
%>
</%def>

##
## if we geocoded stuff on some other pages, we'll cache them here via .js 
##
<%def name="cache_geocodes_in_browser(cache, prefix='js')">
<script src="${prefix}/autocomplete.js"></script>
<script>
    var pc = new PlaceCache();
    %for c in cache:
    pc.add(new PlaceDAO("${c['label']}", "${c['lat']}", "${c['lon']}", true));
    %endfor
</script>
</%def>

##
## do things like escape & in intersection names, etc...
##
<%def name="prep_url_params(params, no_space=False, url_escape=False, spell_and=False)">
<%
    ret_val = params
    try:
        # step 1: convert & in intersection names, ala F Blvd & Z Ave to %26
        if no_space:
            ret_val = ret_val.replace('&', '%26')
        else:
            ret_val = ret_val.replace(' & ', ' %26 ')

        # step 2: replace all instance of %26 with 'and'
        if spell_and:
            ret_val = ret_val.replace('%26', 'and')

        # step 3: order is important ... want to convert to %26 above before escaping...else you'll get an &amp; in you name...
        if url_escape:
            # use escape method from urllib 
            import urllib
            ret_val = urllib.quote(ret_val) 
    except:
        pass
    return ret_val
%>
</%def>

<%def name="get_first_param(param_name, def_val=None)">
<%
    from ott.utils import html_utils
    return html_utils.get_first_param(request, param_name, def_val)
%>
</%def>

<%def name="has_url_param(param_name)">
<%
    from ott.utils import html_utils
    ret_val = False
    loc = html_utils.get_first_param(request, param_name)
    if loc:
        ret_val = True
    return ret_val
%>
</%def>

<%def name="get_locale(def_val='en')">
<%
    from ott.utils import html_utils
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

<%def name="pretty_date_from_ms(ms)"><%
    from ott.utils import date_utils
    pretty = date_utils.pretty_date_from_ms(ms)
%>${pretty}</%def>

<%def name="print_year()"><%
    from ott.utils import date_utils
    dt = date_utils.get_day_info()
%>${dt['year']}</%def>

<%def name="time_stamp()"><%
    from time import strftime as time
%><!-- built: ${'%m/%d/%Y at %H:%M' | time} --></%def>

<%def name="month_options(selected)">
    %for m in (_(u'January'), _(u'February'), _(u'March'), _(u'April'), _(u'May'), _(u'June'), _(u'July'), _(u'August'), _(u'September'), _(u'October'), _(u'November'), _(u'December')):
        <option value="${loop.index + 1}" ${'selected' if m == selected or str(loop.index+1) == str(selected) else ''} >${m}</option>
    %endfor
</%def>
<%def name="month_select(selected)"><select name="month" tabindex="7" id="month" class="regular">
    ${month_options(selected)}
    </select></%def>

<%def name="month_abbv_options(selected)">
    %for m in (_(u'Jan'), _(u'Feb'), _(u'Mar'), _(u'Apr'), _(u'May'), _(u'Jun'), _(u'Jul'), _(u'Aug'), _(u'Sep'), _(u'Oct'), _(u'Nov'), _(u'Dec')):
        <option value="${loop.index + 1}" ${'selected' if  m == selected or str(loop.index+1) == str(selected) else ''}>${m}</option>
    %endfor
</%def>
<%def name="month_abbv_select(selected)"><select name="month" tabindex="7" id="month" class="regular">
    ${month_abbv_options(selected)}
</select></%def>

<%def name="day_options(selected)">
    %for d in range(1, 32):
        <option value="${d}" ${'selected' if d == selected else ''}>${d}</option>
    %endfor
</%def>
<%def name="day_select(selected=1)"><select name="day" tabindex="8" id="day" class="regular">
    ${day_options(selected)}
    </select></%def>

<%def name="link_or_strong(strong_label, link_label, make_strong, url, l_bracket='[', r_bracket=']')">
    %if make_strong:
        <span class="toggle">${strong_label}</span>
    %else:
        <a href="${url}" class="toggle">${link_label}</a>
    %endif
</%def>

<%def name="list_to_str(list, sep=', ')">${sep.join(list)}</%def>

<%def name="alerts_inline_icon_link(img_url='/global/img/icon-alert.png')">
    <a href="#alerts" class="stop-alert"><img src="${url_domain()}${img_url}" alt="${_(u'Service alert at this stop')}" title="${_(u'Service alert at this stop')}" /></a>
</%def>

<%def name="alerts(alert_list, img_url='/global/img/icon-alert.png')">
    %if alert_list and len(alert_list) > 0:
    <div id="alerts">
        %for a in alert_list:
        ${alert_content(a, img_url)}
        %endfor
    </div>
    %endif
</%def>

<%def name="alert_content(alert, img_url='/images/triptools/alert.png')">
    <p><img src="${url_domain()}${img_url}"/>
        %if header_text in alert and alert['header_text']:
        <b>${alert['header_text']}</b><br />
        %endif
        <b>${alert['route_short_names']}: </b> ${alert['description_text']} 
        %if alert['pretty_start_date']:
        <small>${_(u'As of')} ${alert['pretty_start_date']} <a href="${alert['url']}" target="#">${_(u'More')}</a></small>
        %endif
    </p>
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

<%def name="or_bar(show_or=True)">
    %if show_or:
    <div class="or">
        <div class="or-bar"></div>
        <div class="or-text">${_(u'Or')}</div>
    </div>
    %endif
</%def>
