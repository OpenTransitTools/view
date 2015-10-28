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
    ## some whacked code for clearing form data and setting default from / to value, etc... could be improved
    if place is None:
        if clear is None:
        	clear = ''
        place = clear.strip()
        clear_js = "doClear(this, '" + place + "');"
    else:
        clear_js = ""
    
%>
    <input type="hidden" id="${id}_coord" name="${name}Coord" value="${coord}" />
    <input type="text" id="${id}" name="${name}" value="${place}" size="45" maxlength="80" tabindex="${tab}" class="regular" onFocus="${clear_js} doClassHighlight(this);" onBlur="tpDoText(this,'${clear}'); tpDoClassRegular(this);"/>
</%def>

##
## adds callbacks to trip forms
##
<%def name="dynamic_forms_js()">
    <script type="text/javascript">
    try {
        var forms = new DynamicForms("${_(u'Maximum walk')}", "${_(u'Maximum bicycle')}");
        forms.switch_mode();
        forms.add_mode_callback();
    } catch(e) {
        console.log(e);
    }
    </script>
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
<div id="plantrip" class="row">
    <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
        <form name="itin" id="itin_id" method="GET" action="${form_action}" class="triptools-form">
            <fieldset class="normal">
                <label for="from">${_(u'From')}</label>
                ${input_form('from', 'from', from_form_def, 1, params['fromPlace'], params['fromCoord'], is_mobile)}
                <p class="help" id="from-gps"><small><a href="#" onclick="getFromGPS();">${_(u'Use current location')}</a> ${_(u'or')} ${_(u'enter an address, intersection, landmark or Stop ID')}</small></p>
            </fieldset>

            <fieldset class="normal">
                <label for="going">${_(u'To')}</label>
                ${input_form('to', 'going', to_form_def, 2, params['toPlace'], params['toCoord'], is_mobile)}
                <p class="help" id="to-gps"><small><a href="#" onclick="getToGPS();">${_(u'Use current location')}</a> ${_(u'or')} ${_(u'enter an address, intersection, landmark or Stop ID')}</small></p>
            </fieldset>

            <fieldset class="departwhen">
                <label for="when">${_(u'When')}</label>
                <select name="Arr" id="depart" tabindex="3"  class="regular" onchange="tpShowTimeControls(this.selectedIndex);">
                    ${arrive_depart_form_option(params['Arr'], is_mobile)}
                </select>
            </fieldset>

            <fieldset class="departwhen-units">
                <div class="row">
                    <div class="col-xs-6">
                        <select name="Hour" id="Hour" tabindex="4" class="regular">
                            %for i in range(1, 13):
                                ${util.option(i, i, util.compare_values(params['Hour'], i))}
                            % endfor
                        </select>

                        <b>:</b>

                        <select name="Minute" id="Minute" tabindex="5"class="regular">
                            %for i in range(60):
                                ${util.option(i, str(i).rjust(2,'0'), util.compare_values(params['Minute'], i))}
                            % endfor
                        </select>

                        <select name="AmPm" id="AmPm" tabindex="6" class="regular">
                            ${util.option('am', _(u'am'), params['is_am'])}
                            ${util.option('pm', _(u'pm'), not params['is_am'])}
                        </select>
                    </div><!-- .col -->
                    <div class="col-xs-6">
                        <div id="departwhen-date">
                            <b>${_(u'on')}</b>
                            <select name="month" id="Month" tabindex="7" class="regular">
                                ${util.month_abbv_options(params['month'])}
                            </select>
                            <select name="day" id="Day" tabindex="8" class="regular">
                                ${util.day_options(params['day'])}
                            </select>
                        </div>
                    </div><!-- .col -->
                </div><!-- .row -->
            </fieldset>


            <h3>${_(u'Trip preferences (optional)')}</h3>
            <div class="row">
                <div class="col-xs-4">
                    <fieldset class="preferences">
                        <label for="trip-transfers">${_(u'Show me the')}</label>
                        <select id="trip-transfers" name="optimize" tabindex="9" class="regular">
                            ${optimize_form_option(params['optimize'], is_mobile)}
                        </select>
                        %if not is_mobile:
                        <div class="form-help">
                            <p><small>${_(u"Fewer transfers may result in a longer trip.")}</small></p>
                        </div>
                        %endif
                    </fieldset>
                </div><!-- .col -->
                <div class="col-xs-4"> 
                    <fieldset class="preferences">
                        <label for="trip-walkdistance">${_(u'Maximum walk')}</label>
                        <select id="trip-walkdistance" name="Walk" tabindex="10" class="regular">
                            ${walk_form_option(params['Walk'], is_mobile)}
                        </select>
                        %if not is_mobile:
                        <div class="form-help">
                            <p><small>${_(u"How far are you willing to walk to/from your stop?")}</small></p>
                        </div>
                        %endif
                    </fieldset>
                </div><!-- .col -->
                <div class="col-xs-4"> 
                    <fieldset class="preferences">
                        <label for="trip-modetype">${_(u'Travel by')}</label>
                        <select id="trip-modetype" name="mode" tabindex="11" class="regular">
                            ${mode_form_option(params['mode'], is_mobile)}
                        </select>
                        %if not is_mobile:
                        <div class="form-help">
                            <p><small>${_(u"Which travel methods do you prefer?")}</small></p>
                        </div>
                        %endif
                    </fieldset> 
                </div><!-- .col -->
            </div><!-- .row -->                        

        


            <fieldset class="submit">
                ${form.get_extra_params_hidden_inputs()}
                <input name="submit" tabindex="13" type="submit" value="${_(u'Get directions')}" id="submit" class="submit" title="${_(u'Plan your trip')}" onclick="tpGoogleAnalytics(_gaq, ['_trackEvent', 'TripPlanner', 'Submit', ' Advanced Trip Planner submit']);" />
                <div class="mapcheckbox-wrap">
                    <input type="checkbox" id="mapcheckbox" tabindex="12" name="mapit" value="A"/>
                    <label for="mapcheckbox" class="mapcheckbox-label">${_(u'Use interactive map')}</label>
                </div>
            </fieldset>
        </form>
    </div><!-- .col -->
</div><!-- .row -->
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
