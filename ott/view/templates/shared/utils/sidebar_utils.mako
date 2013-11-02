## -*- coding: utf-8 -*-
##
## routines for different sidebar content
##
<%namespace name="util" file="/shared/utils/misc_util.mako"/>


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


<%def name="stop(stop, extra_params)">
    <aside id="aside" class="aside">
        <h2>${_(u'See also')}</h2>  
        <ul class="links">
            <li><a href="nearest_service_form.html?stop_id=${stop['stop_id']}&name=${stop['name']}&lat=${stop['lat']}&lon=${stop['lon']}${extra_params}">${_(u'Find nearest service to')} ${stop['name']}</a></li>
        </ul>
        <p class="feedback"><a href="feedback.html?app=stop&stop_id=${stop['stop_id']}${extra_params}">${_(u'Having problems? Click here for technical support.')}</a></p>
    </aside>
    <!-- end #sidebar -->
</%def>
