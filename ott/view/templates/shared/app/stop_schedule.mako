## -*- coding: utf-8 -*-
<%page args="is_mobile=False"/>
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="meta" file="/shared/utils/meta_utils.mako"/>
<%namespace name="page" file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%namespace name="ssu"  file="/shared/utils/stop_schedule_utils.mako"/>
<%
    extra_params = util.get_extra_params()

    stop = stop_sched['stop']
    name = su.make_name_id(stop)
    stop_params = su.make_url_params(stop)
%>
<div class="standardheader">
    <h1>
        <a href="stop_select_form.html"><i class="fa-ss-outline h1icon"></i></a> ${_(u'Schedule for')}${page.stop_schedule(name, extra_params, stop_params, stop, stop_sched['has_alerts'])}<br/>
        <small>${su.stop_title(stop)}</small>
    </h1>
</div><!-- .standardheader -->

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            %if is_mobile:
            <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
            %else:
            <div class="col-xs-12">
            %endif
                ${ssu.svc_key_tabs(stop, html_tabs, extra_params + '#triptool')}
                ${ssu.schedule_sort_by_links(stop, extra_params)}
                ${ssu.schedule_all_routes_link(stop_sched, extra_params)}
                ${ssu.schedule_render(stop_sched, html_tabs['pretty_date'], extra_params)}
                ${util.alerts(alerts)}
                ${su.nearby_stops_link(stop, extra_params)}
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
