## -*- coding: utf-8 -*-

<%def name="route_select_form(url, route_list, analytics='', tabindex='9', instructions='')">
    <!-- BEGIN route_select_form() --> 
    <form action="${url}" class="form-style" method="get">
        <fieldset>
            <label for="route">${_(u"Select a line:")}</label>
            <select id="route" name="route">
            %if route_list:
            %for r in route_list:
                <option value="${r['id']}">${r['name']}</option>
            %endfor
            %endif
            </select>
            <p class="instructions">
                ${instructions}
                &nbsp;
            </p>
        </fieldset>
        <fieldset class="submit2">
            <input tabindex="${tabindex}" type="submit" id="submit" value='${_(u"Select")}' onclick="${analytics}" />
        </fieldset>
    </form>
    <!-- END route_select_form() --> 
</%def>
