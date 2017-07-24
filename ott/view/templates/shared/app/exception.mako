## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    feedback_url = '//trimet.org/contact/tripfeedback.htm'
%>
<div class="standardheader">
    <h1><a href="stop_select_form.html"><i class="fa-ss-outline h1icon"></i></a> ${_(u'Stops & Stations')}</h1>    
</div><!-- .standardheader --> 
<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                ${util.error_msg(extra_params, feedback_url)}
            </div><!-- .col -->
        </div><!-- .row -->        
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
