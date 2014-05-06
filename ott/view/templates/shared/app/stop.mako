## -*- coding: utf-8 -*-
<%page args="is_mobile=False"/>
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="side" file="/shared/utils/sidebar_utils.mako"/>
<%namespace name="meta" file="/shared/utils/meta_utils.mako"/>
<%namespace name="page" file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    name = su.make_name_id(stop)
    stop_params = su.make_url_params(stop)
    has_alerts = su.has_alerts(stop)

    from ott.view.utils import agency_template
    url = agency_template.make_url_template()
%>
${page.stop(name, extra_params, stop_params, stop, has_alerts)}
<h2>${util.name_city_str_from_struct(stop)}</h2>

<div class="group">
    <div class="left-column">

        %for r in stop['routes']:
        <h3 class="tight">${r['name']}</h3>
        <p>
            %if 'direction' in r:
            ${r['direction']}<br/>
            %endif
            <a href="${url.get_arrivals_url(stop_id=stop['stop_id'], route_id=r['route_id'], device=is_mobile)}">${_(u'Next arrivals')}</a>
                &nbsp;&bull;&nbsp; <a href="stop_schedule.html?stop_id=${stop['stop_id']}&route=${r['route_id']}${extra_params}" title="${_(u'Show schedules for this stop')}.">${_(u'Schedule')}</a> 
                &nbsp;&bull;&nbsp; <a href="${url.get_route_url(route_id=r['route_id'], device=is_mobile)}" title="${_(u'Show map and schedules for this line')}.">${_(u'Route info')}</a>
        </p>
        %endfor

        %if len(stop['routes']) > 1:
        <h3 class="tight">${_(u'All routes')}</h3>
        <p>
            <a class="hide" href="${url.get_arrivals_url(stop_id=stop['stop_id'], device=is_mobile)}">${_(u'Next arrivals')}</a>
                &nbsp;&bull;&nbsp; <a href="stop_schedule.html?stop_id=${stop['stop_id']}${extra_params}">${_(u'Schedule')}</a>
        </p>
        %endif

        %if len(stop['amenities']) > 1:
        <h4 class="tight">${_(u'Amenities')}</h4>
        <ul class="small">
            %for a in stop['amenities']:
            <li>${_(a).capitalize()}</li>
            %endfor
        </ul>
        %endif

        %if has_alerts:
            ${util.alerts(stop['alerts'])}
        %endif
    </div><!-- end .left-column -->

    <div class="right-column">
        ${su.stop_map(stop['name'], stop['stop_id'], stop['lon'], stop['lat'], extra_params, is_mobile)}
        ${util.plan_a_trip_links(stop['name'], stop['lon'], stop['lat'], extra_params)}
    </div><!-- end .right-column -->
</div><!-- end .group -->
