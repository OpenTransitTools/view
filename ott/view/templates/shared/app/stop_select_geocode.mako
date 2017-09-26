## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    sub_msg = form.geocoder_msg_str(geocoder_results, geo_place)
%>

${su.simple_header(title=_(u'Uncertain location'), sub_title=sub_msg)}

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