## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()

    from ott.view.utils import agency_template
    url = agency_template.make_url_template()
    rte_url_tmpl = url.desktop_route_url
    more_link = not util.has_url_param('show_more')
%>

<div class="standardheader wide">
    <h1>
        <a href="stop_select_form.html"><i class="tmfa-ss-outline h1icon"></i></a> ${_(u'Stops & Stations')}
    </h1>
</div><!-- .standardheader -->

<div class="fullwidth">
    <div class="contentcontainer compact">
        <div class="row">
            <div class="col-xs-12">
                <h3 class="hcenter">${_(u'Stops near')} <b>${util.map_place_link(place)}</b></h3>
                <p>&nbsp;</p>
                ${su.stops_list(nearest, rte_url_tmpl, more_link, params, extra_params)}
                ${util.cache_geocodes_in_browser(cache)}
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
