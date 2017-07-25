## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="meta" file="/shared/utils/meta_utils.mako"/>
<%namespace name="page" file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()

    from ott.view.utils import agency_template
    url = agency_template.make_url_template()
    rte_url_tmpl = url.desktop_route_url
    more_link = not util.has_url_param('show_more')
%>

<div class="standardheader">
    <h1>
        <a href="stop_select_form.html"><i class="fa-ss-outline h1icon"></i></a> ${_(u'Stops & Stations')} <br/>
        <small>${_(u'Stops near')} ${util.map_place_link(place)}</small>
    </h1>
</div><!-- .standardheader -->

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                ${su.stops_list(nearest, rte_url_tmpl, more_link, params, extra_params)}
                ${util.cache_geocodes_in_browser(cache)}
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
