## -*- coding: utf-8 -*-
<%namespace name="util" file="/shared/utils/misc_utils.mako"/>
<%namespace name="form" file="/shared/utils/form_utils.mako"/>
<%def name="route_select_form(url, route_list, analytics='')">
    <!-- BEGIN route_select_form() --> 
    <form action="${url}" method="get" class="triptools-form">
        <fieldset>
            ${form.get_extra_params_hidden_inputs()}
            <label for="route">${_(u"Select a line")}:</label>
            <select id="route" name="route" onFocus="doClassHighlight(this);" onBlur="doClassRegular(this);" class="regular">
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

<%def name="route_stop_dropdown(route_stops, analytics='')">
<div id="stoplist">
    % for d in route_stops['directions']:
    <form action="stop.html" method="get" class="triptools-form">
        <fieldset>
            ${form.get_extra_params_hidden_inputs()}
            <label for="${d['direction_name']}">${d['direction_name']}</label>
            <select name="stop_id" id="${d['direction_name']}" onfocus="doClassHighlight(this);" onblur="doClassRegular(this);" class="regular">
                % for s in d['stop_list']['stops']:
                <option value="${s['stop_id']}">${s['name']} (#${s['stop_id']})</option>
                % endfor
            </select>
        </fieldset>
        <fieldset>
            <input type="submit" class="submit" value="${_(u'Select stop')}" id="select" />
        </fieldset>
    </form>
    %if not loop.last:
    <div class="or">
        <div class="or-bar"></div>
        <div class="or-text">${_(u'Or')}</div>
    </div>
    %endif
    % endfor
</div>
</%def>
