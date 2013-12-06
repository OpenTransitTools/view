## -*- coding: utf-8 -*-
##
## routines for different sidebar content
##
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>

<%def name="tc_pr_lr_wes_mall()">
    <!-- begin #sidebar -->
    <aside id="aside" class="aside">
        <h2>${_(u'Related')}</h2>  
        <ul class="links">
            <li><a href="${util.url_domain()}/transitcenters/index.htm">${_(u'Transit Centers')}</a></li>
            <li><a href="${util.url_domain()}/max/stations/index.htm">${_(u'MAX Light Rail stations')}</a></li>
            <li><a href="${util.url_domain()}/wes/stations.htm">${_(u'WES Commuter Rail stations')}</a></li>
            <li><a href="${util.url_domain()}/parkandride/index.htm">${_(u'Park & Ride lots')}</a></li>
            <li><a href="${util.url_domain()}/portlandmall/index.htm">${_(u'Portland Transit Mall')}</a></li>
        </ul>
    </aside>
    <!-- end #sidebar -->
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
    </div><!-- end #trimet-ads -->
    %endif
</%def>

##
##  show a few links on the sidebar (w/icons)
##  help: specify the url (default to trip planner)
##  imap: link to the imap
##  feedback: link to feedback too ... caller provides
##  onClick="_gaq.push(['_trackEvent', 'Trip Planner Ads','ClickTo', '/contact/']); 
## 
##
<%def name="help_map_feedback(map_params='map', feedback_params=None, feedback_txt=None, help_url='/tripplanner/trip-help.htm')">
    <div id="sidebar-icons">
        <p class="helptips"><a href="${util.url_domain()}${help_url}" target="#"><span>${_(u'Help/tips')}</span></a></p>
        <p class="showonmap"><a href="http://ride.trimet.org?mapit=I&submit&${map_params}" target="#" title="${_(u'View on Interactive Map')} (${_(u'High-speed connection recommended')})"><span>${_(u'Show this trip on Interactive Map')}</span></a></p>
        %if feedback_params and feedback_txt:
             <p class="feedbackreport"><a href="/feedback.html?app=${feedback_params}"><span>${_(u'Feedback/report a problem')} ${feedback_txt}</span></a></p>
        %endif
    </div><!-- end #sidebar-icons -->
</%def>


##
## make the stop landing page (right) sidebar
##
<%def name="stop(stop, extra_params)">
<%
    subject = su.str_title(stop)
    message = '<a href="{0}">{1}</a>'.format(request.url, subject)
%>
    <aside id="aside" class="aside">
        <h2>${_(u'See also')}</h2>  
        <ul class="links">
            <li><a href="nearest_service_form.html?stop_id=${stop['stop_id']}&name=${stop['name']}&lat=${stop['lat']}&lon=${stop['lon']}${extra_params}">${_(u'Find nearest service to')} ${stop['name']}</a></li>
        </ul>
        <p class="feedback"><a target="_blank" href="${util.trimet_feedback_url(subject, message)}">${_(u'Having problems? Click here for technical support.')}</a></p>
    </aside>
    <!-- end #sidebar -->
</%def>
