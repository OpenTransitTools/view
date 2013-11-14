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
            ${input_form('from', 'Address, intersection, landmark or Stop ID', 'from', 1, params['fromPlace'], params['fromCoord'], is_mobile)}
            %if is_mobile:
            <p id="from-instructions" style="display:block;" class="instructions">${_(u'Enter address, intersection, landmark or Stop ID')}</p>
            <p id="from-gps" style="display:none;" class="instructions"><a href="#" onclick="getFromGPS();">${_(u'Use my current GPS location')}</a></p>
            %endif 
        </fieldset>

        <fieldset>
            <label for="going">${_(u'To')}</label>
            ${input_form('to', 'Address, intersection, landmark or Stop ID', 'going', 2, params['toPlace'], params['toCoord'], is_mobile)}
            %if is_mobile:
            <p id="to-instructions" style="display:block;" class="instructions">${_(u'Enter address, intersection, landmark or Stop ID')}</p>
            <p id="to-gps" style="display:none;" class="instructions"><a href="#" onclick="getToGPS();">${_(u'Use my current GPS location')}</a></p>
            %endif 
        </fieldset>

        <fieldset class="departwhen">
            <label for="when" class="hide">${_(u'When')}:</label>
            <select name="Arr" id="depart" tabindex="3"  onchange="showTimeControls(this.selectedIndex);" onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${arrive_depart_form_option(params['Arr'], is_mobile)}
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
                ${optimize_form_option(params['optimize'], is_mobile)}
            </select>
            %if not is_mobile:
            <div class="form-help">
                <div class="form-help-popup-onright">
                    <p>${_(u"The quickest trips usually involve transferring between buses and trains and walking a short distance. You can choose 'fewest transfers' if you prefer not to transfer, but your trip will probably take longer.")}</p>
                </div>
            </div>
            %endif
        </fieldset>
        <fieldset class="preferences">
            <label for="trip-options">${_(u'Maximum walk')}</label>
            <select name="Walk" tabindex="10"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${walk_form_option(params['Walk'], is_mobile)}
            </select>
            %if not is_mobile:
            <div class="form-help">
                <div class="form-help-popup-onright">
                    <p>${_(u"Here, you can specify how far you are willing to walk to and from the bus stop or rail station. Note: If set to less than 1 mile, some trips may not be possible.")}</p>
                </div>
            </div>
            %endif
        </fieldset>
        <fieldset class="preferences">
            <label for="trip-options">${_(u'Travel by')}</label>
            <select name="mode" tabindex="11"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                ${mode_form_option(params['mode'], is_mobile)}
            </select>
            %if not is_mobile:
            <div class="form-help">
                <div class="form-help-popup-onright">
                    <p>${_(u"Most trips involve a combination of buses and trains. You can specify bus-only or train-only, but keep in mind that some trips may not be possible as a result. To plan a bike + transit trip, use the Map Trip Planner.")}</p>
                </div>
            </div>
            %endif
        </fieldset>
        <div><a href="${util.url_domain()}/tripplanner/trip-help.htm" onclick="_gaq.push(['_trackEvent', 'Trip Planner Ads', 'ClickTo', '/tripplanner/trip-help.htm']);" class="trip-help">${_(u'Help')}</a></div>
    </div><!-- end #plantrip-right -->
    </form>
</div><!-- end #plantrip -->
</%def>

<%def name="input_form(name, clear, id, tab, place, coord, is_mobile=False)">
    <%
        if place is None:
            if is_mobile is False:
                place = _(clear)
            else:
                place = ''
    %>
    <input type="hidden" id="${id}_coord" name="${name}Coord" value="${coord}" />
    <input type="text"   id="${id}" name="${name}" value="${place}" tabindex="${tab}" onFocus="doClear(this,'${_(clear)}');" onBlur="doText(this,'${_(clear)}'); clear_tp_element('${id}_coord');" class="regular" size="45" maxlength="80" />
    %if not is_mobile:
    <div class="form-help">
        <div class="form-help-popup-onright">
            <p>${_(u"You can type in an address, intersection, landmark or Stop ID here. For the best results, don't include a city, state or ZIP code.")}</p>
        </div>
    </div>
    %endif
</%def>

<%def name="arrive_depart_form_option(sel_key, is_mobile=False)">
<%
    opts = [ 
        {
            "k": "D",
            "v": _(u'Depart after')
        },
        {
            "k": "A",
            "v": _(u'Arrive by')
        },
        {
            "k": "L",
            "v": _(u'Late as possible')
        },
        {
            "k": "E",
            "v": _(u'Early as possible')
        },
    ]
    for o in opts:
        util.option(o['k'], o['v'], sel_key == o['k'])
%>
</%def>


<%def name="optimize_form_option(sel_key, is_mobile=False)">
<%
    opts = [ 
        {
            "k": "QUICK",
            "v": _(u'Quickest trip')
        },
        {
            "k": "TRANSFERS",
            "v": _(u'Fewest transfers')
        }
    ]
    for o in opts:
        util.option(o['k'], o['v'], sel_key == o['k'])
%>
</%def>


<%def name="walk_form_option(sel_key, is_mobile=False)">
<%
    opts = [ 
        {
            "k": "160",
            "v": _(u'1/10 mile')
        },
        {
            "k": "420",
            "v": _(u'1/4 mile')
        },
        {
            "k": "840",
            "v": _(u'1/2 mile')
        },
        {
            "k": "1260",
            "v": _(u'3/4 mile')
        },
        {
            "k": "1609",
            "v": _(u'1 mile')
        },
        {
            "k": "3219",
            "v": _(u'2 miles')
        },
        {
            "k": "4828",
            "v": _(u'3 miles')
        },
        {
            "k": "8047",
            "v": _(u'5 miles')
        },
        {
            "k": "16093",
            "v": _(u'10 miles')
        },
    ]
    for o in opts:
        util.option(o['k'], o['v'], util.compare_values(sel_key, o['k']))
%>
</%def>


<%def name="mode_form_option(sel_key, is_mobile=False)">
<%
    opts = [ 
        {
            "k": "TRANSIT,WALK",
            "v": _(u'Bus or train')
        },
        {
            "k": "TRAINISH,BICYCLE",
            "v": _(u'Train only')
        },
        {
            "k": "BUSISH,WALK",
            "v": _(u'Bus only')
        },
        {
            "k": "TRANSIT,BICYCLE",
            "v": _(u'Bike to Transit')
        },
        {
            "k": "TRAINISH,BICYCLE",
            "v": _(u'Bike and Train only')
        },
        {
            "k": "WALK",
            "v": _(u'Walk only')
        },
   ]
    for o in opts:
        util.option(o['k'], o['v'], sel_key == o['k'])
%>
</%def>


<%def name="gps_form_scriptlet()">
<script>
    // for trip planner page
    function checkgps()
    {
        if (navigator.geolocation) 
        {  
            // if browser supports geolocation, hide instructions and show GPS link instead
            document.getElementById('from-instructions').style.display = 'none';
            document.getElementById('from-gps').style.display = 'block';
            document.getElementById('to-instructions').style.display = 'none';
            document.getElementById('to-gps').style.display = 'block';
        }
    }
    function getFromGPS()
    {
        // Get location no more than 1 minute old. 60000 ms = 1 minute.
        navigator.geolocation.getCurrentPosition(showFromGPS, showError, {enableHighAccuracy:true,maximumAge:0});
        _gaq.push(['_trackEvent', 'GPS', 'Submit', 'Mobile Trip Planner GPS submit']);
    }
    function showFromGPS(position)
    {
        document.forms['itin'].elements['from'].value = position.coords.latitude + ', ' + position.coords.longitude;
    }
    function getToGPS()
    {
        // Get location no more than 1 minute old. 60000 ms = 1 minute.
        navigator.geolocation.getCurrentPosition(showToGPS, showError, {enableHighAccuracy:true,maximumAge:0});
        _gaq.push(['_trackEvent', 'GPS', 'Submit', 'Mobile Trip Planner GPS submit']);
    }
    function showToGPS(position)
    {
        document.forms['itin'].elements['to'].value = position.coords.latitude + ', ' + position.coords.longitude;
    }
    function showError(error)
    {
        alert('${_("Please make sure your GPS setting is turned on for this browser")} (' + error.code + ')' );
    }
</script>
</%def>


<%def name="clear_tp_element_scriptlet()">
    <script>
        function clear_tp_element(id)
        {
            try
            {
                var fm = document.getElementById(id)
                fm.value = ""
            }
            catch(e)
            {
            }
        }
    </script>
</%def>
