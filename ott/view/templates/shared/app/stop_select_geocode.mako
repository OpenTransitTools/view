## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="side" file="/shared/utils/sidebar_utils.mako"/>
<%namespace name="meta" file="/shared/utils/meta_utils.mako"/>
<%namespace name="page" file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()
%>

<div class="standardheader">
    <h1>
        <a href="stop_select_form.html"><i class="fa-ss-outline h1icon"></i></a> ${_(u'Uncertain location')}<br/>
        <small>${form.geocoder_msg(geocoder_results, geo_place)}</small>
    </h1>
</div><!-- .standardheader -->

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                ${su.geocode_form(geocoder_results, geo_place)}
                ${form.autocomplete_search_input()}
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->

${form.select_form_scriptlet()}
${form.autocomplete_css_includes()}
${form.autocomplete_js_includes()}
${form.gps_form_scriptlet()}