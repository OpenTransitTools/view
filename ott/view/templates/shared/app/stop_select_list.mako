## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%namespace name="rs"   file="/shared/utils/route_select_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    route_name = route_stops['route']['name']
%>

${su.simple_header()}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12">
                <h2>Select a ${route_name} stop</h2>
                ${rs.route_stop_dropdown(route_stops)}
            </div><!-- .col -->
        </div><!-- .row -->        
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
