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


<div class="standardheader">
    <h1><a href="stop_select_form.html"><img src="${util.url_domain()}/global/img/icon-stopsstations.png" class="mode-icon" alt="Stops and Stations icon" /></a>${name}</h1>
    <div class="first"><p>${su.stop_title(stop)}</p></div>
</div><!-- .standardheader -->

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-sm-7 col-md-8 col-lg-7">

                %for r in stop['routes']:
                <h2>${r['name']}</h2>
                <p>
                    %if 'direction' in r:
                    ${r['direction']}<br/>
                    %endif
                    <a href="${url.get_arrivals_url(stop_id=stop['stop_id'], route_id=r['route_id'], device=is_mobile)}" title="${_(u'Get real-time arrival information from TransitTracker')}" class="route-icons"><img src="${util.url_domain()}/global/img/icon-transittracker.png" alt="${_(u'Next arrivals')}" /><br />
                        ${_(u'Next arrivals')}</a>

                    <a href="stop_schedule.html?stop_id=${stop['stop_id']}&month=${stop['date_info']['month']}&day=${stop['date_info']['day']}&route=${r['route_id']}${extra_params}" title="${_(u'Show schedule for this stop/station')}" class="route-icons"><img src="${util.url_domain()}/global/img/icon-schedule.png" alt="${_(u'Schedule')}" /><br />
                        ${_(u'Schedule')}</a>

                    <a href="${url.get_route_url(route_id=r['route_id'], device=is_mobile)}" title="${_(u'Show route map and schedules for this line')}" class="route-icons"><img src=${util.url_domain()}/global/img/icon-routeinfo.png alt="${_(u'Route info')}" /><br />
                        ${_(u'Route info')}</a>
                </p>
                %endfor

                %if len(stop['routes']) > 1:
                <h2>${_(u'All routes')}</h2>
                <p>
                    <a href="${url.get_arrivals_url(stop_id=stop['stop_id'], device=is_mobile)}" class="route-icons"><img src="${util.url_domain()}/global/img/icon-transittracker.png" alt="${_(u'Next arrivals')}" /><br />
                        ${_(u'Next arrivals')}</a>
                    <a href="stop_schedule.html?stop_id=${stop['stop_id']}&month=${stop['date_info']['month']}&day=${stop['date_info']['day']}${extra_params}" alt="${_(u'Schedule')}" class="route-icons"><img src="${util.url_domain()}/global/img/icon-schedule.png" alt="${_(u'Schedule')}" /><br />
                        ${_(u'Schedule')}</a>
                </p>
                %endif

                %if len(stop['amenities']) > 1:
                <p>&nbsp;</p>
                <h4>${_(u'Amenities')}</h4>
                <ul>
                    %for a in stop['amenities']:
                    <li>${_(a)}</li>
                    %endfor
                </ul>
                %endif

                %if has_alerts:
                    ${util.alerts(stop['alerts'])}
                %endif
            </div><!-- .col -->

            <div class="col-xs-12 col-sm-5 col-md-4 col-lg-4">
                ${su.stop_map(stop['name'], stop['stop_id'], stop['lon'], stop['lat'], extra_params, is_mobile)}
                ${util.plan_a_trip_links(stop['name'], stop['lon'], stop['lat'], extra_params)}
            </div><!-- .col -->
        </div><!-- .row -->        
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->



