import simplejson as json

from ott.view.model import Model

import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)


class ModelMock(Model):
    def get_stop_schedule_single(self, route):   return get_json('stop_schedule_single.json')
    def get_stop_schedule_multiple(self, route): return get_json('stop_schedule_multiple.json')

    def get_alerts(self, routes):   return get_json('alerts.json')

    def get_route_stops_list(self): return get_json('route_stop_list.json')
    def get_routes(self):           return get_json('route.json')
    def get_stop(self):             return get_json('stop.json')



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

