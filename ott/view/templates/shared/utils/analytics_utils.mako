## -*- coding: utf-8 -*-
##
## routines for making ga skinny
##
<%def name="ga_init(account='UA-688646-3')">
<script type="text/javascript">
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', '${account}', 'auto');
    ga('send', 'pageview');
</script>
</%def>

##
## event call to GA
## _gaq.push(['_trackEvent', 'TripPlanner', 'Submit', ' Advanced Trip Planner submit']);
##
<%def name="event(app, evt, desc)">onClick="_gaq.push(['_trackEvent', '${app}', '${evt}', '${desc}']);"</%def>
<%def name="empty_method()"></%def>
<%def name="trip_submit()"><% event('TripPlanner', 'Submit', 'Trip Planner submit') %></%def>


select_route=event('StopsStations', 'Submit', 'MainForm Select-a-line submit')
find_stop=event('StopsStations', 'Submit', 'MainForm Search submit')
trip_submit=event('TripPlanner', 'Submit', 'Trip Planner submit')
trip_adv_submit=event('TripPlanner', 'Submit', 'Advanced Trip Planner submit')
