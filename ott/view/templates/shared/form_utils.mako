##
##  
##
<%namespace name="util"  file="/shared/util.mako"/>
<%namespace name="help"  file="/shared/help_utils.mako"/>

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
                <option value="${l['name']}::${l['lat']},${l['lon']}::${l['city']}">${util.name_city_str(l['name'], l['city'], l['type_name'])}</option>
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
<%def name="search_input(name, place=None, clear=None, size='43', maxlength='80', id='newloc')">
        <%
           if clear is None:
               clear = _(u'Address, intersection, landmark or Stop ID')
           if place is None:
               place = clear
        %>
        <!-- Text box for re-geocoding a string -->
        <fieldset>
            <label for="geocode_form">${name}:</label>
            <input type="text" name="place" value="${place}" size="${size}" maxlength="${maxlength}" id="${id}" class="regular" onFocus="doClear(this,'${_(clear)}'); doClassHighlight(this);" onBlur="doText(this,'${_(clear)}'); doClassRegular(this);" />
            <div class="form-help">
                ${help.form_help_right()}
            </div>
        </fieldset>
</%def>


##
## search submit BUTTON
##
<%def name="search_submit(name=None, tab=2, analytics=None)">
        <% 
        if name is None:
            name = _(u'Select')
        %>
        <fieldset>
            ## TODO: analytics -- onClick="_gaq.push(['_trackEvent', 'StopsStations', 'Submit', 'MainForm Search submit']);
            <input name="submit" class="submit" type="submit" value="${name}" tabindex="${tab}"/>

            ## TODO: Jonathan -- what is geocode_highslide supposed to look like?
            ## ${help.geocode_highslide()}
        </fieldset>
</%def>

#
# planner form
#
<%def name="input_form(name, clear, id, tab, place, coord)">
    <%
        if place == None:
            place = _(clear)
    %>
    <input type="hidden" id="${id}_coord" name="${name}Coord" value="${coord}" />
    <input type="text"   id="${id}" name="${name}" value="${place}" tabindex="${tab}" onFocus="doClear(this,'${_(clear)}');" onBlur="doText(this,'${_(clear)}'); clear_tp_element('${id}_coord');" class="regular" size="45" maxlength="80" />
    <div class="form-help">
        <div class="form-help-popup-onright">
            <p>${_(u"You can type in an address, intersection, landmark or Stop ID here. For the best results, don't include a city, state or ZIP code.")}</p>
        </div>
    </div>
</%def>

