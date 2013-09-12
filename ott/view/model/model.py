import simplejson as json
import urllib
import logging
log = logging.getLogger(__file__)

from ott.view.model.base import Base

class Model(Base):
    def get_routes(self, get_params, **kwargs):
        #import pdb; pdb.set_trace() 
        # TODO ..
        return self.stream_json('http://127.0.0.1:34443/routes', get_params)

    def get_route_stops(self, get_params, **kwargs): 
        return self.stream_json('http://127.0.0.1:34443/route_stops', get_params)

    def get_stop(self, get_params, **kwargs):
        return self.stream_json('http://127.0.0.1:34443/stop', get_params)

    def get_stop_schedule(self, get_params, **kwargs):
        ret_val = self.stream_json('http://127.0.0.1:34443/stop_schedule', get_params)
        return ret_val

    def get_plan(self, get_params, **kwargs):
        return self.stream_json('http://127.0.0.1:34443/plan_trip', get_params)


def main():
    m=Model()
    print m.get_stop_schedule_single()
    print m.get_stop_schedule_multiple()
    print m.get_stop_schedule_by_time()
    routes=m.get_routes()['routes']
    for r in routes:
        print r


if __name__ == '__main__':
    main()
