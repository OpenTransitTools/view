## -*- coding: utf-8 -*-
##
## routines for different sidebar content
##
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%namespace name="plib" file="/shared/utils/planner_utils.mako"/>


<%def name="tc_pr_lr_wes_mall(msg='Stop related page')">
## moved this into stop_select_form as it only shows on that page
</%def>

##
## loop through any adverts 
##
<%def name="sidebar_adverts(adverts=None)">
    %if adverts:
    <div id="trimet-ads">
        %for a in adverts:
        ${a['content'] | n}
        %endfor
    </div><!-- .trimet-ads -->
    %endif
</%def>

##
##  show a few links on the sidebar (w/icons)
##  help: specify the url (default to trip planner)
##  imap: link to the imap
##  feedback: link to feedback too ... caller provides
##  onClick="_gaq.push(['_trackEvent', 'Trip Planner Ads','ClickTo', '/contact/']); 
##  , plan['params']['feedback_url'], plan['params']['feedback_txt']
##
<%def name="planner(plan, help_url='/tripplanner/trip-help.htm')">
    <div id="sidebar-icons">
        ##<p class="helptips"><a href="${util.url_domain()}${help_url}"><span>${_(u'Help/tips')}</span></a></p>
        <p class="showonmap"><a href="http://ride.trimet.org?mapit=I&submit&${plan['params']['map_planner']}"><span>${_(u'Show this trip on Interactive Map')}</span></a></p>
        <p class="feedbackreport"><a href="${util.trimet_feedback_url(plib.str_title(plan), plib.str_description(plan))}" target="_blank"><span>${_(u'Having problems? Click here for technical support.')}</span></a></p>
    </div><!-- end #sidebar-icons -->
</%def>

##
## planner support pages ... no plan yet
## 
<%def name="planner_support_page(help_url='/tripplanner/trip-help.htm')">
	<p class="feedback"><a href="${util.trimet_feedback_url(_(u"Having trouble with trip planner pages, like the geocoder..."))}" target="_blank"><span>${_(u'Having problems? Click here for technical support.')}</span></a></p>
</%def>


##
## make the stop landing page (right) sidebar
##
<%def name="stop(stop, extra_params)">
    ##<div class="col-xs-12">
        ##    <p>&nbsp;</p>
        ##    <p class="feedback"><a href="${util.trimet_feedback_url(su.str_title(stop), _(u'Stop landing page'))}"><span>${_(u'Having problems? Click here for technical support.')}</span></a></p>
    ##</div><!-- .col -->
</%def>
