## -*- coding: utf-8 -*-
<%page args="is_mobile=False"/>
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%namespace name="meta" file="/shared/utils/meta_utils.mako"/>
<%namespace name="page" file="/shared/utils/pagetype_utils.mako"/>
<%namespace name="su"   file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    sns = _(u'Stops & Stations')
%>

<div class="standardheader">
    <h1><a href="stop_select_form.html"><i class="fa-ss-outline h1icon"></i></a> ${sns}</h1>
</div><!-- .standardheader -->  

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                ${su.stop_select_form()}
                ${form.autocomplete_search_input()}
                <%include file="stop_related_links.mako"/>
            </div><!-- .col -->
        </div><!-- .row -->

    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->

<style type="text/css">
.content h2 { /* hide unhelpful heading */
    display: none;
}
.content form.triptools-form fieldset label { /* match h2 */
    font-size: 24px;
    font-weight: 300;
    line-height: 1em;
    color: #333;
    padding: .5em 0;
}
@media only screen and (min-width: 768px) { /* sm screens and up */
    .content form.triptools-form fieldset label {
        font-size: 32px;
    }
}
</style>

${form.select_form_scriptlet()}
${form.autocomplete_css_includes()}
${form.autocomplete_js_includes()}
${form.gps_form_scriptlet()}
