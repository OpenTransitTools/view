##
## 
##
<%namespace name="util"  file="/shared/util.mako"/>
<%namespace name="help"  file="/shared/help_utils.mako"/>

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


##
## search form
##
<%def name="search_input(clear='')">
        <!-- Text box for re-geocoding a string -->
        <fieldset>
            <label>${_(u'Re-type location')}:</label>
            <input type="text" name="place" value="${place}" size="43" maxlength="80" id="newloc" class="regular" onFocus="doClassHighlight(this);" onBlur="doClassRegular(this);" />
            <div class="form-help">
                ${util.form_help_right()}
            </div>
        </fieldset>
</%def>


##
## search form
##
<%def name="search_submit()">
        <fieldset>
            <input name="submit" tabindex="4" type="submit" value="${_(u'Continue')}" class="submit" />
            ${help.geocode_highslide()}
        </fieldset>
</%def>