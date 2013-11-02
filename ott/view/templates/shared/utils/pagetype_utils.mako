##
## these methods set the sub-menu pointer, the link, etc...
##
<%def name="stop_select(name='', extra_params='', src='me')">
    <%def name="stations_selected()">class="selected"</%def>
    <h1 class="stopsstations-icon">
        <a href="stop_select_form.html?${src}${extra_params}" title="${_(u'Stops & Stations')} ${_(u'Home')}" class="homelink"><span class="visuallyhidden">${_(u'Stops & Stations')} ${_(u'Home')}</span></a>
        ${name}
    </h1>
</%def>


<%def name="stop(name='', extra_params='', src='me')">
</%def>


<%def name="trip_planner(name='', extra_params='', src='me')">
</%def>