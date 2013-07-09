import simplejson as json
import urllib
import logging
log = logging.getLogger(__file__)

from ott.view.model.base import Base


class Mock(Base):
    def get_stop_schedule_single(self, route): return get_json('stop_schedule_single.json')
    def get_stop_schedule_multiple(self, route=None): return get_json('stop_schedule_multiple.json')

    def get_alerts(self, routes, stops=None): return get_json('alerts.json')

    def get_route_stops(self, route): return get_json('route_stop.json')
    def get_routes(self): return get_json('routes.json')
    def get_stop(self):   return get_json('stop.json')

    def get_plan(self, get_params, **kwargs):
        ''' @todo: MODE strings should come from gtfsdb code...
        '''
        # TODO -- better stuff below for mock testing...
        #import pdb; pdb.set_trace()
        '''
        if 'mode' in kwargs:
            if kwargs['mode'] in ('S','STREAM'):  return stream_json('http://127.0.0.1:34443/plan_trip', get_params)
            if kwargs['mode'] in ('T','TEST'):    return get_json('x.json')
            if kwargs['mode'] in ('A','ALERTS'):  return get_json('plan_alerts.json')

            if    Model.WALK == kwargs['mode']: return get_json('plan_walk.json') 
            elif  Model.BIKE == kwargs['mode']: return get_json('plan_bike.json') 
            elif  Model.RAIL == kwargs['mode']: return get_json('plan_rail.json') 
            elif  Model.STREETCAR == kwargs['mode']: return get_json('plan_streetcar.json') 
            elif  Model.GONDOLA == kwargs['mode'] or  Model.TRAM in kwargs['mode']: return get_json('plan_tram.json') 
            elif  Model.TRANSIT in kwargs['mode'] and Model.BIKE in kwargs['mode']: return get_json('plan_bike_transit.json') 
            else: return stream_json('http://127.0.0.1:34443/plan_trip')
        else:
            return stream_json('http://127.0.0.1:34443/plan_trip', get_params)
        '''
            #TODO - work on error return get_json('plan_error.json')
        return stream_json('http://127.0.0.1:34443/plan_trip', get_params)

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


PATH='ott/view/static/test/'
def get_json(file):
    ''' utility class to load a static .json file for mock'ing a service
    '''
    ret_val={}
    try:
        with open(file) as f:
            ret_val = json.load(f)
    except:
        try:
            path="{0}{1}".format(PATH, file)
            with open(path) as f:
                ret_val = json.load(f)
        except:
            log.info("Couldn't open file : {0} (or {1})".format(file, path))

    return ret_val


def stream_json(u, args):
    ''' utility class to stream .json
    '''
    ret_val={}
    url = "{0}?{1}".format(u, args)
    stream = urllib.urlopen(url)
    otp = stream.read()
    ret_val = json.loads(otp)
    return ret_val

