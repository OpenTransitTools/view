import simplejson as json
import logging
log = logging.getLogger(__file__)

from ott.view.model import Model


class ModelMock(Model):
    def get_stop_schedule_single(self, route): return get_json('stop_schedule_single.json')
    def get_stop_schedule_multiple(self, route=None): return get_json('stop_schedule_multiple.json')

    def get_alerts(self, routes, stops=None): return get_json('alerts.json')

    def get_route_stops(self, route): return get_json('route_stop.json')
    def get_routes(self): return get_json('routes.json')
    def get_stop(self):   return get_json('stop.json')

    def get_plan(self, **kwargs):
        ''' @todo: MODE strings should come from gtfsdb code...
        '''
        if 'mode' in kwargs:
            if    Model.WALK == kwargs['mode']: return get_json('plan_walk.json') 
            elif  Model.BIKE == kwargs['mode']: return get_json('plan_bike.json') 
            elif  kwargs['mode'].contains(Model.TRANSIT) and kwargs['mode'].contains(Model.BIKE):
                  return get_json('plan_bike_transit.json') 
            else: return get_json('plan_transit.json') 
        else:
            return get_json('plan_error.json')

    def get_adverts(self, **kwargs):
        mode = True if kwargs['mode'].contains(Model.TRAIN) else False
        if mode:
            return get_json('adverts_rail.json') 
        else:
            return get_json('adverts_bus.json') 


def main():
    m=ModelMock()
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


PATH='docs/mock/'
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

