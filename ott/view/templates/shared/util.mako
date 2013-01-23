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
