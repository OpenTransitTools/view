## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="su"    file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    feedback_url = '//trimet.org/contact/tripfeedback.htm'
%>

${su.simple_header()}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                ${util.error_msg(extra_params, feedback_url)}
            </div><!-- .col -->
        </div><!-- .row -->        
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
