import simplejson as json
import urllib
import logging
log = logging.getLogger(__file__)

from ott.view.model.base import Base
from ott.utils import object_utils


class Model(Base):
    def get_routes(self, get_params, **kwargs):
        return self.stream_json('routes', get_params)

    def get_route_stops(self, get_params, **kwargs): 
        return self.stream_json('route_stops', get_params)

    def get_stops_near(self, get_params, **kwargs):
        return self.stream_json('stops_near', get_params)

    def get_stop(self, get_params, **kwargs):
        return self.stream_json('stop', get_params)

    def get_stop_schedule(self, get_params, **kwargs):
        ret_val = self.stream_json('stop_schedule', get_params)
        return ret_val

    def get_plan(self, get_params, **kwargs):
        return self.stream_json('plan_trip', get_params)

    def get_geocode(self, search):
        val = object_utils.to_str(search)
        return self.stream_json('geocode', "place={0}".format(val))

    def get_adverts(self, get_params, **kwargs):
        ret_val = self.stream_json('adverts', get_params)
        return ret_val


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
