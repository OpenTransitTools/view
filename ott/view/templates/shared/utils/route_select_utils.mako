## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%def name="route_select_form(url, route_list, analytics='')">
    <!-- BEGIN route_select_form() --> 
    <form action="${url}" method="get" class="triptools-form">
        <fieldset>
            ${form.get_extra_params_hidden_inputs()}
            <label for="route">${_(u"Select a line")}:</label>
            <select id="route" name="route">
            %if route_list:
            %for r in route_list:
                <option value="${r['route_id']}">${r['name']}</option>
            %endfor
            %endif
            </select>
        </fieldset>
        <fieldset>
            <input type="submit" class="submit" value='${_(u"Select")}' onclick="${analytics}" />
        </fieldset>
    </form>
    <!-- END route_select_form() -->
</%def>
