## -*- coding: utf-8 -*-
<%page args="is_mobile=False, title=''"/>
<%namespace name="util"  file="/shared/utils/misc_utils.mako"/>
<%namespace name="form"  file="/shared/utils/form_utils.mako"/>
<%namespace name="side"  file="/shared/utils/sidebar_utils.mako"/>
<%namespace name="meta"  file="/shared/utils/meta_utils.mako"/>
<%namespace name="page"  file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="plib"  file="/shared/utils/planner_utils.mako"/>
<%namespace name="pform" file="/shared/utils/planner_form_utils.mako"/>
<%namespace name="an"    file="/shared/utils/analytics_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    title = "{} {}".format(_(u'Your trip on'), util.get_agency_ini(plus_str=None))
%>
${form.gps_form_scriptlet(id=geo_type, form='ambig')}
${page.tripplanner_css()}
${form.autocomplete_css_includes()}

${plib.simple_header(title)}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                ${page.trip_planner(_(u'Uncertain Location'), extra_params, 'form')}

                <%def name="bottom()"></%def>
                <h2 class="error">
                    ${form.geocoder_msg(geocoder_results, geo_place, geo_type)}
                </h2>
                ${pform.geocode_form(geocoder_results, geo_place, geo_type)}
                ${form.autocomplete_js_includes()}
                ${form.autocomplete_search_input('#' + geo_type)}
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
