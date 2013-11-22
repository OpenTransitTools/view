## -*- coding: utf-8 -*-
## 
## library of routines that do input forms and drop down lists 
## (geocoder mostly)
##
<%namespace name="util"  file="/shared/utils/misc_util.mako"/>
<%namespace name="help"  file="/shared/utils/help_utils.mako"/>
<%namespace name="an"    file="/shared/utils/analytics_utils.mako"/>

##
## javascript for clearing out an html element field...
## (used in GEO <input> form elements ... hidden geo data element e.g., placeCoord)
##
<%def name="clear_element_scriptlet()">
<script>
    function clear_element(id) {
        try {
            var fm = document.getElementById(id)
            fm.value = ""
        }
        catch(e) {}
    }
</script>
</%def>

#
# search list form
# Scrolling List of Possible Locations
#
<%def name="search_list(name=None, list=None, show_or=True, show_submit=True, id='id', size=1)">
    <%
        if name is None:
            name = _(u'Select a location')
    %>
    %if list and len(list) > 0:
        <!-- Ambiguous address list - choose a specific address leading to nearest stops -->
        <fieldset>
            <label>${name}:</label>
            <select size="${size}" name="place" class="regular" id="${id}" onFocus="doClassHighlight(this);" onBlur="doClassRegular(this);" />
                %for l in list:
                <option value="${l['name']}::${l['lat']},${l['lon']}::${l['city']}">${util.name_city_str(l['name'], l['city'], l['type_name'], l['stop_id'])}</option>
                %endfor
            </select>
        </fieldset>
        %if show_or:
            ${search_submit()}
        %endif
        %if show_or:
        <div class="or">
            <div class="or-bar"></div>
            <div class="or-text">${_(u'Or')}</div>
        </div>
        %endif
    %endif
</%def>

##
## search input form
##
<%def name="search_input(name, place=None, clear=None, id='place', coord='', size='67', maxlength='100')">
<%
   if clear is None:
       clear = _(u'Address, intersection, landmark or Stop ID')
   if place is None:
       place = clear
%>
    ${clear_element_scriptlet()}
    <!-- Text box for re-geocoding a string -->
    <fieldset>
        <label for="geocode_form">${name}:</label>
        <input type="hidden" id="${id}_coord" name="${id}Coord" value="${coord}"/>
        <input type="text"   id="${id}" name="${id}" value="${place}" size="${size}" maxlength="${maxlength}" class="regular" onFocus="clear_element('${id}_coord'); doClear(this,'${_(clear)}'); doClassHighlight(this);" onBlur="doText(this,'${_(clear)}'); doClassRegular(this);"/>  
        <div class="form-help">
            ${help.form_help_right()}
        </div>
    </fieldset>
</%def>

#
# autocomplete: instance creation for the jQuery autocomplete...
#
<%def name="autocomplete_search_input(id='#place')">
    <script>
    // main entry 
    $(function(){
        stop = new SOLRAutoComplete('${id}');
        stop.enable_ajax();

        function stop_geo_callback(sel)
        {
            $(this.geo_div).val(sel.solr_doc.lat + ',' + sel.solr_doc.lon);
        }
        stop.geo_div = "${id}_coord";
        stop.select_callback = stop_geo_callback;
        
    });
    </script>
</%def>

#
# autocomplete: CSS and JS includes...
#
<%def name="autocomplete_css_includes()">
    <link href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet"/>
    <link href="/css/autocomplete.css" rel="stylesheet"/>
</%def>
<%def name="autocomplete_js_includes()">
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <script src="/js/autocomplete.js"></script>
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
            ## TODO: Jonathan -- what is geocode_highslide supposed to look like?
            ## ${help.geocode_highslide()}
        </fieldset>
</%def>

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

