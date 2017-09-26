## -*- coding: utf-8 -*-
## 
## library of routines that do input forms and drop down lists 
## (geocoder mostly)
##
<%namespace name="util"  file="/shared/utils/misc_utils.mako"/>
<%namespace name="help"  file="/shared/utils/help_utils.mako"/>
<%namespace name="an"    file="/shared/utils/analytics_utils.mako"/>

<%def name="select_form_scriptlet(id='place')">
    <script type="text/javascript">
    function select_form() {
        try {
            document.getElementById('${id}').focus();
        }
        catch(e) {}
    }
    </script>
</%def>

#
# search list form
# Scrolling List of Possible Locations
#
<%def name="search_list(name=None, list=None, show_or=True, show_submit=True, id='place-list', param_name='place', size=1)">
    <%
        if name is None:
            name = _(u'Select a location')
    %>
    %if list and len(list) > 0:
        <!-- Ambiguous address list - choose a specific address leading to nearest stops -->
        <fieldset>
            <label for="${id}">${name}:</label>
            <input type="hidden" name="geo_type" value="${id}"/>
            <select size="${size}" id="${id}" name="${param_name}" onFocus="doClassHighlight(this);" onBlur="doClassRegular(this);" class="regular">
                %for l in list:
                <option value="${l['name']}::${l['lat']},${l['lon']}::${l['city']}">${util.name_city_stopid(l['name'], l['city'], l['type'], l['stop_id'])}</option>
                %endfor
           </select>
        </fieldset>
        %if show_or:
            ${search_submit()}
        %endif
    %endif
</%def>

##
## search input form
##
<%def name="search_input(name, place=None, clear=None, id='place', coord='', size='67', maxlength='100', clear_form=True, is_mobile=False)">
<%
   if clear is None:
       clear = ' '
   if place is None:
       place = ''
%>
    <!-- Text box for re-geocoding a string -->
    <fieldset>
        <label for="${id}">${name}:</label>
        <input type="hidden" name="geo_type" value="${id}"/>
        <input type="hidden" id="${id}_coord" name="${id}Coord" value="${coord}"/>
        <input type="text" id="${id}" name="${id}" value="${place}" size="${size}" maxlength="${maxlength}" class="regular" />
        <p id="${id}-gps" class="help"><small><a href="#" onclick="getGPS();">${_(u'Use current location')}</a> ${_(u'or')} ${_(u'enter an address, intersection, landmark or Stop ID')}</small></p>
    </fieldset>
</%def>


#
# autocomplete: CSS and JS includes...
#
<%def name="autocomplete_js_includes(prefix='js')">
    <script type="text/javascript" src="${prefix}/jquery.js"></script>
    <script type="text/javascript" src="${prefix}/jquery-ui-autocomplete.js"></script>
    <script type="text/javascript" src="${prefix}/autocomplete.js"></script>
</%def>

<%def name="planner_form_js_includes(prefix='js')">
    <script type="text/javascript" src="${prefix}/text_planner.js"></script>
    <script type="text/javascript" src="${prefix}/dynamic_forms.js"></script>
</%def>

<%def name="autocomplete_css_includes(prefix='css')">
    <link href="${prefix}/autocomplete.css" rel="stylesheet"/>
</%def>


##
## auto complete - localize name
## (TODO - this won't work, ala AJAX ... so what to do?)
##
<%def name="autocomplete_localize_place_name()">
        function localized_place_name_format(name, city, type, id)
        {
            var ret_val = name;
            try {
                var stop = ''
                if(type == 'stop')
                    stop = " (${_(u'Stop ID')} " + id + ")";
                ret_val = name + city + stop;
            }
            catch(e) {
            }
            return ret_val;
        }
        stop.place_name_format = localized_place_name_format;
</%def>

##
## autocomplete: instance creation for the jQuery autocomplete...
##
<%def name="autocomplete_search_input(id='#place')">
    <% solr_url = util.get_ini_param('ott.solr_url', '/solr/select') %>
    <script type="text/javascript">
    // main entry 
    $(function(){
        var remove_title = "${_(u'remove')}";
        var cache = new PlaceCache(remove_title, true);
        var stop = new SOLRAutoComplete('${id}', '${solr_url}', cache);
        stop.enable_ajax();
        stop.geo_div = "${id}_coord";
        ${autocomplete_localize_place_name()}
    });
    </script>
</%def>

##
## search submit BUTTON
##
<%def name="search_submit(name=None, tab=2, analytics=None)">
<% 
    if name is None:
        name = _(u'Select')
    if analytics is None:
        analytics = an.empty_method
%>
        <fieldset>
            <input name="submit" class="submit" type="submit" value="${name}" tabindex="${tab}" ${analytics()}/>
        </fieldset>
</%def>

#
# If we can't find a place in the geocoder, or if we find multiple places, you'll see this msg...
#
<%def name="geocoder_msg_str(geocoder_results, geo_place, geo_type=None)"><%
    ret_val = ""
    if geo_type:
        geo_type = "<i>{}</i>".format(_(geo_type))
    else:
        geo_type = ''

    if geocoder_results and len(geocoder_results) > 0:
        ret_val = "{} {} {} {}: {}".format(_(u'We found multiple'), geo_type, _(u'locations'), _(u'for'), geo_place)
    else:
        ret_val = "{} {} {} {}: {}".format(_(u'We cannot find a'), geo_type, _(u'location'), _(u'for'), geo_place)
    return ret_val
%></%def>

<%def name="geocoder_msg(geocoder_results, geo_place, geo_type=None)">${geocoder_msg_str(geocoder_results, geo_place, geo_type)}</%def>

#
# hidden param to indicate whether some input has already been geocoded
#
<%def name="has_geocode_hidden(val='false')">
        <input type="hidden" name="has_geocode" value="${val}"/>
</%def>

#
# misc hidden params to insert into a <form> element
#
<%def name="get_extra_params_hidden_inputs()">
<%
    loc = util.get_locale(None)
%>
    %if loc:
        <input type="hidden" name="_LOCALE_" value="${loc}"/>
    %endif
</%def>

#
# url params to hidden inputs
#
<%def name="url_params_to_hidden_inputs(req, skips=[])">
<%
    from ott.utils import html_utils
    pdict = html_utils.params_to_dict(req)
%>
    %for k,v in pdict.items():
    %if k and k not in skips:
        <input type="hidden" name="${k}" value="${v}"/>
    %endif
    %endfor
</%def>


##
## GPS stuff
###
<%def name="gps_form_scriptlet(id='place', form='geocode')">
<script type="text/javascript" >
    function checkgps()
    {
        if(navigator.geolocation)
        {
            // if browser supports geolocation, hide instructions and show GPS link instead
            try {
                document.getElementById('${id}-instructions').style.display = 'none';
            } catch(e) {}
            try {
                document.getElementById('${id}-gps').style.display = 'block';
            } catch(e) {}
        }
    }
    function getGPS()
    {
        // Get location no more than 1 minute old. 60000 ms = 1 minute.
        navigator.geolocation.getCurrentPosition(showGPS, showError, {'enableHighAccuracy':true, 'timeout':10000, 'maximumAge':180000});
        _gaq.push(['_trackEvent', 'GPS', 'Submit', 'Mobile Trip Planner GPS submit']);
    }
    function showGPS(position)
    {
        document.forms['${form}'].elements['${id}'].value = position.coords.latitude + ', ' + position.coords.longitude;
        try {
        document.forms['${form}'].elements['${id}Coord'].value = position.coords.latitude + ', ' + position.coords.longitude;
        } catch(e) {}
    }
    function showError(error)
    {
        alert('${_("Please make sure your GPS setting is turned on for this browser")} (' + error.code + ')' );
    }
</script>
</%def>
