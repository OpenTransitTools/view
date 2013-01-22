## -*- coding: utf-8 -*-

<%def name="url_domain()">http://trimet.org</%def>

<%def name="form(url='', method='get', class_='form-style')"></%def>
<%def name="end_form()"></%def>
<%def name="select(name='route', stuff=[], options='')"></%def>
<%def name="route_select_options()"></%def>
<%def name="url_for(controller='main', action='route_stops_list')"></%def>


<%def name="month_select(selected=3)"><select name="month" tabindex="8" >
    %for m in (_(u'January'), _(u'February'), _(u'March'), _(u'April'), _(u'May'), _(u'June'), _(u'July'), _(u'August'), _(u'September'), _(u'October'), _(u'November'), _(u'December')):
        %if m == selected or loop.index+1 == selected:
            <option selected="selected" value="${loop.index + 1}">${m}</option>
        %else:
            <option value="${loop.index + 1}">${m}</option>
        %endif
    %endfor
    </select></%def>


<%def name="day_select(selected=1, len=31)"><select name="day" tabindex="9" >
        <option value="1">1</option>
        <option value="1">31</option>
    </select></%def>
