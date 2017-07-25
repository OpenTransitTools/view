## -*- coding: utf-8 -*-
<%page args="is_mobile=False, title='x'"/>
<%namespace name="util"  file="/shared/utils/misc_utils.mako"/>
<%namespace name="page"  file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="plib"  file="/shared/utils/planner_utils.mako"/>
<%namespace name="pform" file="/shared/utils/planner_form_utils.mako"/>
<%namespace name="form"  file="/shared/utils/form_utils.mako"/>
<%
    extra_params = util.get_extra_params()
%>

${page.tripplanner_css()}
${form.autocomplete_css_includes()}
${form.autocomplete_js_includes()}
${form.planner_form_js_includes()}
${form.select_form_scriptlet('from')}
${pform.gps_form_scriptlet()}

${plib.simple_header(title)}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12">
                ##
                ## main content
                ##
                ${pform.planner_form()}
                ${pform.autocomplete_trip_planner()}
                ${pform.dynamic_forms_js()}
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
