import simplejson as json
import urllib
import logging
log = logging.getLogger(__file__)

from ott.utils import html_utils
from ott.utils import transit_utils
from ott.utils.modes import Modes

from ott.view.model.base import Base

class Mock(Base):
    def get_alerts(self, routes, stops=None): return self.get_json('alerts.json')

    def get_routes(self, get_params, **kwargs): return self.get_json('routes.json')
    def get_route_stops(self, get_params, **kwargs): return self.get_json('route_stop.json')

    def get_stop(self, get_params, **kwargs):
        '''
        routes = request.model.get_routes(request.query_string, **request.params)
        if stop and routes:
            stop['routes'] = routes
            stop['alerts'] = request.model.get_alerts(routes, stop['id'])
        '''
        return self.get_json('stop.json')

    def get_stop_schedule(self, get_params, **kwargs):
        has_route = False
        if 'route' in kwargs:
            has_route = transit_utils.is_valid_route(kwargs['route'])

        if has_route:
            return self.get_json('stop_schedule_single.json') 
        else:
            return self.get_json('stop_schedule_multiple.json')


    def get_plan(self, get_params, **kwargs):
        #import pdb; pdb.set_trace() 
        return self.stream_json('plan_trip', get_params)


    def Xget_plan(self, get_params, **kwargs):
        ''' @todo: MODE strings should come from gtfsdb code...
        '''
        #import pdb; pdb.set_trace()
        if 'mode' in kwargs:
            if kwargs['mode'] in ('T','TEST'):    return self.get_json('x.json')
            if kwargs['mode'] in ('A','ALERTS'):  return self.get_json('plan_alerts.json')

            if    Modes.WALK == kwargs['mode']: return self.get_json('plan_walk.json') 
            elif  Modes.BIKE == kwargs['mode']: return self.get_json('plan_bike.json') 
            elif  Modes.RAIL == kwargs['mode']: return self.get_json('plan_rail.json') 
            elif  Modes.STREETCAR == kwargs['mode']: return self.get_json('plan_streetcar.json') 
            elif  Modes.GONDOLA == kwargs['mode'] or  Modes.TRAM in kwargs['mode']: return self.get_json('plan_tram.json') 
            elif  Modes.TRANSIT in kwargs['mode'] and Modes.BIKE in kwargs['mode']: return self.get_json('plan_bike_transit.json') 

        return self.get_json('plan_bike_transit.json')
        #return stream_json('http://127.0.0.1:34443/plan_trip', get_params)

def main():
    m=Mock()
    #print m.get_stop()
    #print m.get_route_stops_list()
    print m.get_stop_schedule_single()
    print m.get_stop_schedule_multiple()
    print m.get_stop_schedule_by_time()
    routes=m.get_routes()['routes']
    for r in routes:
        print r


if __name__ == '__main__':
    main()

