## -*- coding: utf-8 -*-
<%page args="is_mobile=False"/>
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()
%>

${su.simple_header()}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12">
                ${su.stop_select_form()}
                ${form.autocomplete_search_input()}
                <%include file="stop_related_links.mako"/>
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->

${form.select_form_scriptlet()}
${form.autocomplete_css_includes()}
${form.autocomplete_js_includes()}
${form.gps_form_scriptlet()}
