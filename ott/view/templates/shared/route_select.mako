## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/util.mako"/>
<%def name="route_select_form(url, route_list, analytics='')">
    <!-- BEGIN route_select_form() --> 
    <form action="${url}" method="get" class="triptools-form">
        <fieldset>
            ${util.get_extra_params_hidden_inputs()}
            <label for="route">${_(u"Select a line:")}</label>
            <select id="route" name="route">
            %if route_list:
            %for r in route_list:
                <option value="${r['id']}">${r['name']}</option>
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
