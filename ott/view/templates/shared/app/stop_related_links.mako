## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
    <h3>${_(u'Related')}</h3>
    <div class="row">
        <div class="col-xs-12 col-sm-6">
           <ul class="links">
                <li><a href="${util.url_domain()}/transitcenters/index.htm">${_(u'Transit Centers')}</a></li>
                <li><a href="${util.url_domain()}/max/stations/index.htm">${_(u'MAX Light Rail stations')}</a></li>
                <li><a href="${util.url_domain()}/wes/stations.htm">${_(u'WES Commuter Rail stations')}</a></li>
            </ul>
        </div><!-- .col -->
        <div class="col-xs-12 col-sm-6">
           <ul class="links">
                <li><a href="${util.url_domain()}/parkandride/index.htm">${_(u'Park & Ride lots')}</a></li>
                <li><a href="${util.url_domain()}/portlandmall/index.htm">${_(u'Portland Transit Mall')}</a></li>
            </ul>
        </div><!-- .col -->
    </div><!-- .row (i.e., related)-->
