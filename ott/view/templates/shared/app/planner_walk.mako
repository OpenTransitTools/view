## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="plib" file="/shared/utils/planner_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    itinerary = plib.get_itinerary(plan)
    title = _(u'Your trip instructions')
%>
<script src="${util.url_domain()}/global/js/triptools.js"></script>

##
## main content
##
${plib.simple_header(title)}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12">
                ## CSS customizations for walk directions
                <style>
                    .content .step-number {
                        display: none;
                    }
                    .content ol.walkbike > li {
                        list-style: none;
                    }
                </style>
                %if itinerary:
                    ${plib.render_trip_details(plan)}
                    ${plib.render_itinerary(itinerary, extra_params, True)}
                %else:
                    ${plib.get_error_msg(error, _('Uncertain planner problem'))}
                %endif
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
