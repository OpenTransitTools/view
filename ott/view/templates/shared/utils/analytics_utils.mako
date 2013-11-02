## -*- coding: utf-8 -*-
##
## routines for making ga skinny
##
<%def name="ga_init(account='UA-688646-3')">
<script type="text/javascript">
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', ${account}]);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
</%def>

#
# event call to GA
# _gaq.push(['_trackEvent', 'TripPlanner', 'Submit', ' Advanced Trip Planner submit']);
#
<%def name="event(app, evt, desc)">onClick="_gaq.push(['_trackEvent', '${app}', '${evt}', '${desc}']);"</%def>

<%def name="empty_method()"></%def>
<%def name="trip_submit()"><%event('TripPlanner', 'Submit', 'Trip Planner submit')%></%def>


select_route=event('StopsStations', 'Submit', 'MainForm Select-a-line submit')
find_stop=event('StopsStations', 'Submit', 'MainForm Search submit')
trip_submit=event('TripPlanner', 'Submit', 'Trip Planner submit')
trip_adv_submit=event('TripPlanner', 'Submit', 'Advanced Trip Planner submit')

