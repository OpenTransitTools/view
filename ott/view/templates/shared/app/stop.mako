## -*- coding: utf-8 -*-
<%page args="is_mobile=False"/>
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%
    from ott.view.utils import agency_template
    url = agency_template.make_url_template()
    has_alerts = su.has_alerts(stop)
    extra_params = util.get_extra_params()
%>
<div class="fullwidth">
    <div class="contentcontainer compact">
        <div class="row">
            <div class="col-xs-12 col-sm-7 col-md-8 col-lg-7">

                %for r in stop['routes']:
                <h3>${r['name']}</h3>
                <p>
                    %if 'direction' in r:
                    ${r['direction']}<br/>
                    %endif
                    <a href="//trimet.org/home/stop/${stop['stop_id']}?route=${r['route_id']}" title="${_(u'Get real-time arrival information from TransitTracker')}" class="route-icons"><i class="tmfa-tt-outline"></i><br />
                        ${_(u'Next arrivals')}</a>

                    <a href="stop_schedule.html?stop_id=${stop['stop_id']}&month=${stop['date_info']['month']}&day=${stop['date_info']['day']}&route=${r['route_id']}${extra_params}" title="${_(u'Show schedule for this stop/station')}" class="route-icons"><i class="tmfa-schedule"></i><br />
                        ${_(u'Schedule')}</a>

                    <a href="${url.get_route_url(route_id=r['route_id'], device=is_mobile)}" title="${_(u'Show route map and schedules for this line')}" class="route-icons"><i class="tmfa-map"></i><br />
                        ${_(u'Route info')}</a>
                </p>
                %endfor

                %if len(stop['routes']) > 1:
                <h3>${_(u'All routes')}</h3>
                <p>
                    <a href="//trimet.org/home/stop/${stop['stop_id']}" class="route-icons"><i class="tmfa-tt-outline"></i><br />
                        ${_(u'Next arrivals')}</a>
                    <a href="stop_schedule.html?stop_id=${stop['stop_id']}&month=${stop['date_info']['month']}&day=${stop['date_info']['day']}${extra_params}" alt="${_(u'Schedule')}" class="route-icons"><i class="tmfa-schedule"></i><br />
                        ${_(u'Schedule')}</a>
                </p>
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

        <div class="row">
            <div class="col-xs-12 col-lg-10">
                %if len(stop['amenities']) > 1:
                <p>&nbsp;</p>
                <h4>${_(u'Amenities')}</h4>
                <ul class="small inline">
                    %for a in stop['amenities']:
                    <li>${_(a)}</li>
                    %endfor
                </ul>
                %endif
            </div><!-- .col -->
        </div><!-- .row -->  
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
