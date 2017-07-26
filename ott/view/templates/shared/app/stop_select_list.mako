## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%namespace name="page" file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="rs"   file="/shared/utils/route_select_utils.mako"/>
<%
    extra_params = util.get_extra_params()
%>

${su.simple_header()}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                ${page.stop_select(route_stops['route']['name'], extra_params, 'list')}
                ${rs.route_stop_dropdown(route_stops)}
            </div><!-- .col -->
        </div><!-- .row -->        
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
