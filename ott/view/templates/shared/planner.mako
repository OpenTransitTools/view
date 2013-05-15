<%def name="get_optimize(plan)">
<%
    if plan['optimize'] == 'SAFE':
        optimize = _(u'Safest trip')
    elif plan['optimize'] == 'TRANSFERS':
        optimize = _(u'Fewest transfers')
    else:
        optimize = _(u'Quickest trip')
    return optimize
%>
</%def>

<%def name="get_time(plan, itinerary)">
<%
    if plan['arrive_by']:
        time = itinerary['date_info']['end_time']
    else:
        time = itinerary['date_info']['start_time']
    return time
%>
</%def>

<%def name="get_itinerary(plan)">
<%
    # find target itinerary 
    for itin in plan['itineraries']:
        itinerary = itin
        if itin['selected']:
            break
    return itinerary
%>
</%def>

<%def name="get_depart_arrive(plan)">
<%
    if plan['arrive_by']:
        depart_arrive = _(u'Arrive by')
    else:
        depart_arrive = _(u'Depart after') 
    return depart_arrive
%>
</%def>
