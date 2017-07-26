## -*- coding: utf-8 -*-
<%page args="is_mobile=False, title=''"/>
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="plib" file="/shared/utils/planner_utils.mako"/>
<%
    itinerary = plib.get_itinerary(plan)
    extra_params = util.get_extra_params()
    title = "{} {}".format(_(u'Your trip on'), util.get_agency_ini(plus_str=None))
%>

${plib.simple_header(title)}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12">
                ##
                ## main content
                ##
                ${plib.render_trip_details(plan, itinerary, extra_params)}
                ${plib.render_tabs(plan, extra_params)}
                ${plib.render_itinerary(itinerary, extra_params)}
                ${plib.render_fares(itinerary, util.url_domain() + '/fares/index.htm')}
                ${plib.render_alerts(itinerary)}
                ${plib.render_console(plan, extra_params)}
                ${util.cache_geocodes_in_browser(cache)}
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->

<script src="${util.url_domain()}/scripts/triptools.js"></script>
${plib.set_planner_text_cookie()}
