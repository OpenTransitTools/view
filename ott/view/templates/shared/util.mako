## -*- coding: utf-8 -*-
<%def name="url_domain()">http://trimet.org</%def>
<%def name="form(url='', method='get', class_='form-style')"></%def>
<%def name="end_form()"></%def>
<%def name="select(name='route', stuff=[], options='')"></%def>
<%def name="route_select_options()"></%def>
<%def name="url_for(controller='main', action='route_stops_list')"></%def>

<%def name="month_select(selected)"><select name="month" tabindex="8" >
    %for m in (_(u'January'), _(u'February'), _(u'March'), _(u'April'), _(u'May'), _(u'June'), _(u'July'), _(u'August'), _(u'September'), _(u'October'), _(u'November'), _(u'December')):
        <option value="${loop.index + 1}" ${'selected' if  m == selected or loop.index+1 == selected else ''} >${m}</option>
    %endfor
    </select></%def>

<%def name="day_select(selected=1, len=31)"><select name="day" tabindex="9" >
    %for d in range(1, len+1):
        <option value="${d}" ${'selected' if d == selected else ''}>${d}</option>
    %endfor
    </select></%def>

<%def name="link_or_strong(label, make_strong, url, label_prefix='', l_bracket='[', r_bracket=']')">
    %if make_strong:
        <strong>${label}</strong>
    %else:
        <a href="${url}">${l_bracket}${label_prefix} ${label}${r_bracket}</a>
    %endif
</%def>

<%def name="alerts_inline_icon_link(img_url='/v3/images/m/alert.gif')">
    <a href="#alerts" class="alert"><img border="0" src="${url_domain()}${img_url}" alt="${_(u'See footnote')}" title="${_(u'See footnote')}"/></a>
</%def>

<%def name="alerts(alert_list, img_url='/v3/images/m/alert.gif')">
    %for a in alert_list:
    <div class="planner-alerts">
        <a name="alerts"></a>
        <h3><a href="${url_domain()}/alerts/"><img border="0" src="${url_domain()}${img_url}"/>${_(u'Service Alerts')}</a></h3>
        <h4>${a['name']}</h4>
        <p>
            <span class="alert-icon">${a['description']}</span>
        </p>
    </div>
    %endfor
</%def>