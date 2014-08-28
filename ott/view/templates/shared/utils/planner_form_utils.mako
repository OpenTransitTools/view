## -*- coding: utf-8 -*-
##
## routine(s) for the trip planner form(s)
##
<%namespace name="util"  file="/shared/utils/misc_utils.mako"/>
<%namespace name="form"  file="/shared/utils/form_utils.mako"/>
<%namespace name="plib"  file="/shared/utils/planner_utils.mako"/>
<%namespace name="an"    file="/shared/utils/analytics_utils.mako"/>

<%def name="from_to_img_url(type=None, def_val=False)">
<%
    ret_val = def_val
    if type:
        if 'from' in type:
            ret_val = 'images/triptools/old/start.png'
        elif 'to' in type:
            ret_val = 'images/triptools/old/end.png'
    return ret_val
%>
</%def>


##
## sets up autocomplete for the trip planner from & to form
##
<%def name="autocomplete_trip_planner(fm_id='#from', to_id='#going')">
    <%  solr_url = util.get_ini_param('ott.solr_url', '/solr/select') %>
    <script>
    // main entry 
    $(function(){
        var remove_title = "${_(u'remove')}";
        var cache = new PlaceCache(remove_title, true);

        var fm = new SOLRAutoComplete('${fm_id}', '${solr_url}', cache);
        fm.enable_ajax();
        fm.geo_div = "${fm_id}_coord";

        var to = new SOLRAutoComplete('${to_id}', '${solr_url}', cache);
        to.enable_ajax();
        to.geo_div   = "${to_id}_coord";
    });
    </script>
</%def>

##
## planner ambiguous geocode form(s) 
##
<%def name="geocode_form(geocoder_results, geo_place='', geo_type='place', form_action='planner.html', is_mobile=False)">
<div id="location">
    %if geocoder_results and len(geocoder_results) > 0:
    <form action="${form_action}"  method="GET" name="ambig-list" class="triptools-form">
        ${form.url_params_to_hidden_inputs(request, [geo_type, geo_type + 'Coord'])}
        ${form.has_geocode_hidden('true')}
        ${form.get_extra_params_hidden_inputs()}
        ${form.search_list(name=_(u'Select a location'), list=geocoder_results, id=geo_type+'list', param_name=geo_type)}
    </form>
    ${util.or_bar()}
    %endif

    <form action="${form_action}"  method="GET" name="ambig" class="triptools-form">
        ${form.url_params_to_hidden_inputs(request, [geo_type, geo_type + 'Coord'])}
        ${form.has_geocode_hidden('false')}
        ${form.get_extra_params_hidden_inputs()}
        ${form.search_input(_(u'Re-type location'), geo_place, id=geo_type, clear_form=False, is_mobile=is_mobile)}
        ${form.search_submit(_(u'Continue'), 4, analytics=an.trip_submit)}
        ## TODO: need to add analytic events when customer hit's "ENTER" button / submit
    </form>

    ${util.geocoder_feedback(geo=geo_place, svc='planner_geocode.html?geo_type=from&from=')}
</div>
</%def>

##
## input_form for planner 
## TODO: why this and not form.input_form?
##
<%def name="input_form(name, id, clear, tab, place, coord, is_mobile=False)">
<%
    if place is None:
        place = ''
        clear_js = "doClear(this, '${clear}');"
    else:
        clear_js = ""
    
%>
    <input type="hidden" id="${id}_coord" name="${name}Coord" value="${coord}" />
    <input type="text" id="${id}" name="${name}" value="${place}" size="45" maxlength="80" tabindex="${tab}" class="regular" onFocus="${clear_js} doClassHighlight(this); this.setSelectionRange(0, this.value.length);" onBlur="doText(this,'${clear}'); doClassRegular(this);"/>
    %if not is_mobile:
    <div class="form-help">
        <div class="form-help-popup-onright">
            <p>${_(u"You can type in an address, intersection, landmark or Stop ID here.")}</p>
        </div>
    </div>
    %endif
</%def>

##
## large trip planner form on planner_form.html
##
<%def name="planner_form(form_action='planner.html', is_mobile=False, is_homepage=False, agency='TriMet')">
<%
    from_form_def = ' '
    to_form_def  = ' '
    if is_homepage:
        from_form_def = _(u'From')
        to_form_def   = _(u'To')
%>
<div id="plantrip" class="basic">
    %if is_homepage:
    <h2><b>${_(u'Plan your trip')}</b> ${_(u'on')} ${agency} <span class="secondary" style="font-size:.5em; color:#ccc;">BETA</span></h2>
    <!--<div style="position:absolute; top:1.875em; right:1.5em; width:8em; height:2em; text-align:right;"><a href="/go/cgi-bin/plantrip.cgi" style="font-size:.75em; color:#ccc; border-color:#666;">Use old trip planner</a></div>-->
    %endif 
    %if not is_homepage:
    <!--<div style="position:absolute; top:-1.875em; right:1.5em; width:12em; height:2em; text-align:right;"><a href="/go/cgi-bin/plantrip.cgi" style="color:#fff;">Use old trip planner</a></div>-->
    %endif 
    <form name="itin" id="itin_id" method="GET" action="${form_action}" class="form-style"/>
        <div id="plantrip-left">
            <fieldset class="normal">
                <label for="from" class="homepage-hide">${_(u'From')}</label>
                ${input_form('from', 'from', from_form_def, 1, params['fromPlace'], params['fromCoord'], is_mobile)}
                %if is_mobile:
                <p id="from-instructions" style="display:block;" class="instructions">${_(u'Enter address, intersection, landmark or Stop ID')}</p>
                <p id="from-gps" style="display:none;" class="instructions"><a href="#" onclick="getFromGPS();">${_(u'Use my current GPS location')}</a></p>
                %endif
            </fieldset>

            <fieldset class="normal">
                <label for="going" class="homepage-hide">${_(u'To')}</label>
                ${input_form('to', 'going', to_form_def, 2, params['toPlace'], params['toCoord'], is_mobile)}
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
            <fieldset class="departwhen-units">
                <div id="departwhen-time">
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
                </div>
                <div id="departwhen-date">
                    <span class="homepage-hide">${_(u'on')}</span>
                    <select name="month" id="Month" tabindex="7"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                        ${util.month_abbv_options(params['month'])}
                    </select>
                    <select name="day" id="Day" tabindex="8"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                        ${util.day_options(params['day'])}
                    </select>
                </div>
            </fieldset>
            %if is_homepage:
            <div id="more-options" class="basic">
                <a href="javascript:showTripPlannerAdvanced();"><span>${_(u'More options')} &raquo;</span></a>
            </div>
            %endif
        </div><!-- end #plantrip-left -->

        <div id="plantrip-right" class="basic">
            <p id="trippreferences">${_(u'Trip preferences (optional)')}</p>
            <fieldset class="preferences">
                <label for="trip-transfers">${_(u'Show me the')}</label>
                <select id="trip-transfers" name="optimize" tabindex="9"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                    ${optimize_form_option(params['optimize'], is_mobile)}
                </select>
                %if not is_mobile:
                <div class="form-help">
                    <div class="form-help-popup-onleft">
                        <p>${_(u"The quickest trips usually involve transferring between buses and trains and walking a short distance. You can choose 'fewest transfers' if you prefer not to transfer, but your trip will probably take longer.")}</p>
                    </div>
                </div>
                %endif
            </fieldset>
            <fieldset class="preferences">
                <label for="trip-walkdistance">${_(u'Maximum walk')}</label>
                <select id="trip-walkdistance" name="Walk" tabindex="10"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                    ${walk_form_option(params['Walk'], is_mobile)}
                </select>
                %if not is_mobile:
                <div class="form-help">
                    <div class="form-help-popup-onleft">
                        <p>${_(u"Here, you can specify how far you are willing to walk or bike to and from the bus stop or rail station. Note: If set to less than 1 mile, some trips may not be possible.")}</p>
                    </div>
                </div>
                %endif
            </fieldset>
            <fieldset class="preferences">
                <label for="trip-modetype">${_(u'Travel by')}</label>
                <select id="trip-modetype" name="mode" tabindex="11"  onfocus="doClassHighlight(this);" class="regular" onblur="doClassRegular(this);">
                    ${mode_form_option(params['mode'], is_mobile)}
                </select>
                %if not is_mobile:
                <div class="form-help">
                    <div class="form-help-popup-onleft">
                        <p>${_(u"Most trips involve a combination of buses and trains. You can specify bus-only or train-only, but keep in mind that some trips may not be possible as a result.")}</p>
                    </div>
                </div>
                %endif
            </fieldset>
            <!--<div><a href="${util.url_domain()}/tripplanner/trip-help.htm" onclick="_gaq.push(['_trackEvent', 'Trip Planner Ads', 'ClickTo', '/tripplanner/trip-help.htm']);" class="trip-help">${_(u'Help')}</a></div>-->
            %if is_homepage:
            <span id="less-options">
                <a href="javascript:showTripPlannerAdvanced();"><span>&laquo; ${_(u'Fewer options')}</span></a>
            </span>
            %endif 
        </div><!-- end #plantrip-right -->

        <fieldset class="submit">
            ${form.get_extra_params_hidden_inputs()}
            <input name="submit" tabindex="13" type="submit" value="${_(u'Get directions')} &raquo;" id="submit" title="${_(u'Submit your trip plan information')}" onclick="_gaq.push(['_trackEvent', 'TripPlanner', 'Submit', ' Advanced Trip Planner submit']);" />
            <div id="mapcheckbox-wrap">
                <input type="checkbox" id="mapcheckbox" tabindex="12" name="mapit" value="A"/>
                <label for="mapcheckbox" class="mapcheckbox-label">${_(u'Use Interactive Map')}</label>
            </div>
        </fieldset>
    </form>
</div><!-- end #plantrip -->
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
        }
        ,
        {
            "k": "TRANSFERS",
            "v": _(u'Fewest transfers')
        }
        ,
        {
            "k": "SAFE",
            "v": _(u'Bike friendly trip')
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
            "k": "TRAINISH,WALK",
            "v": _(u'Train only')
        },
        {
            "k": "BUSISH,WALK",
            "v": _(u'Bus only')
        },
        {
            "k": "TRANSIT,BICYCLE",
            "v": _(u'Bike to transit')
        },
        {
            "k": "TRAINISH,BICYCLE",
            "v": _(u'Bike and train only')
        },
        {
            "k": "BICYCLE",
            "v": _(u'Bike only')
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
        navigator.geolocation.getCurrentPosition(showFromGPS, showError, {'enableHighAccuracy':true, 'timeout':10000, 'maximumAge':180000});
        _gaq.push(['_trackEvent', 'GPS', 'Submit', 'Mobile Trip Planner GPS submit']);
    }
    function showFromGPS(position)
    {
        document.forms['itin'].elements['from'].value = position.coords.latitude + ', ' + position.coords.longitude;
    }
    function getToGPS()
    {
        // Get location no more than 1 minute old. 60000 ms = 1 minute.
        navigator.geolocation.getCurrentPosition(showToGPS, showError, {'enableHighAccuracy':true, 'timeout':10000, 'maximumAge':180000});
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
