## -*- coding: utf-8 -*-
##
## routine(s) for the trip planner form(s)
##
<%namespace name="util" file="/shared/utils/misc_util.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="plib"  file="/shared/utils/planner.mako"/>

<%def name="planner_form(form_action='planner.html', is_mobile=False)">
<div id="plantrip" class="group">
    <form name="itin" id="itin_id" method="GET" action="${form_action}" class="form-style"/>
    <div id="plantrip-left">
        <fieldset>
            <label for="from">${_(u'From')}</label>
            ${plib.input_form('from', 'Address, intersection, landmark or Stop ID', 'from', 1, params['fromPlace'], params['fromCoord'])}
        </fieldset>

        <fieldset>
            <label for="going">${_(u'To')}</label>
            ${plib.input_form('to', 'Address, intersection, landmark or Stop ID', 'going', 2, params['toPlace'], params['toCoord'])}
        </fieldset>

        <fieldset class="departwhen">
            <label for="when" class="hide">${_(u'When')}:</label>
            <select name="Arr" id="depart" tabindex="3"  onchange="showTimeControls(this.selectedIndex);" onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${plib.arrive_depart_form_option(params['Arr'])}
            </select>
        </fieldset>
        <fieldset>
            <select name="Hour" id="Hour" tabindex="4"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
            %for i in range(1, 13):
                ${util.option(i, i, util.compare_values(params['Hour'], i))}
            % endfor
            </select>
            <b>:</b>
            <select name="Minute" id="Minute" tabindex="5" onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
            %for i in range(60):
                ${util.option(i, str(i).rjust(2,'0'), util.compare_values(params['Minute'], i))}
            % endfor
            </select>
            <select name="AmPm" id="AmPm" tabindex="6"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${util.option('am', _(u'am'), params['is_am'])}
                ${util.option('pm', _(u'pm'), not params['is_am'])}
            </select>
            <span>${_(u'on')}</span>
            <select name="month" id="Month" tabindex="7"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${util.month_abbv_options(params['month'])}
            </select>
            <select name="day" id="Day" tabindex="8"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${util.day_options(params['day'])}
            </select>
        </fieldset>

        <fieldset class="submit">
            ${form.get_extra_params_hidden_inputs()}
            <input name="submit" tabindex="13" type="submit" value="${_(u'Get directions')} &raquo;" id="submit" title="${_(u'Submit your trip plan information')}" onclick="_gaq.push(['_trackEvent', 'TripPlanner', 'Submit', ' Advanced Trip Planner submit']);" />
            <input type="checkbox" id="mapcheckbox" tabindex="12" title="${_(u'Show trip on an interactive map (broadband/desktop only)')}" name="mapit"  value="A" onclick="doMap();">
            <label for="mapcheckbox" class="mapcheckbox-label" title="${_(u'Show trip on an interactive map (broadband/desktop only)')}">${_(u'Use Interactive Map')}</label>
        </fieldset>
    </div><!-- end #plantrip-left -->

    <div id="plantrip-right">
        <!--<p class="options">${_(u'Trip preferences (optional)')}</p>-->
        <fieldset class="preferences">
            <label for="trip-options">${_(u'Show me the')}</label>
            <select name="optimize" tabindex="9"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${plib.optimize_form_option(params['optimize'])}
            </select>
            <div class="form-help">
                <div class="form-help-popup-onright">
                    <p>${_(u"The quickest trips usually involve transferring between buses and trains and walking a short distance. You can choose 'fewest transfers' if you prefer not to transfer, but your trip will probably take longer.")}</p>
                </div>
            </div>
        </fieldset>
        <fieldset class="preferences">
            <label for="trip-options">${_(u'Maximum walk')}</label>
            <select name="Walk" tabindex="10"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${plib.walk_form_option(params['Walk'])}
            </select>
            <div class="form-help">
                <div class="form-help-popup-onright">
                    <p>${_(u"Here, you can specify how far you are willing to walk to and from the bus stop or rail station. Note: If set to less than 1 mile, some trips may not be possible.")}</p>
                </div>
            </div>
        </fieldset>
        <fieldset class="preferences">
            <label for="trip-options">${_(u'Travel by')}</label>
            <select name="mode" tabindex="11"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${plib.mode_form_option(params['mode'])}
            </select>
            <div class="form-help">
                <div class="form-help-popup-onright">
                    <p>${_(u"Most trips involve a combination of buses and trains. You can specify bus-only or train-only, but keep in mind that some trips may not be possible as a result. To plan a bike + transit trip, use the Map Trip Planner.")}</p>
                </div>
            </div>
        </fieldset>
        <div><a href="${util.url_domain()}/tripplanner/trip-help.htm" onclick="_gaq.push(['_trackEvent', 'Trip Planner Ads', 'ClickTo', '/tripplanner/trip-help.htm']);" class="trip-help">${_(u'Help')}</a></div>
    </div><!-- end #plantrip-right -->
    </form>
</div><!-- end #plantrip -->
</%def>