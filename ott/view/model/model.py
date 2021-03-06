from ott.view.model.base import Base
from ott.utils import object_utils

import logging
log = logging.getLogger(__file__)


class Model(Base):
    def get_routes(self, get_params, **kwargs):
        return self.stream_json('routes', get_params)

    def get_route_stops(self, get_params, **kwargs): 
        return self.stream_json('route_stops', get_params)

    def get_stops_near(self, get_params, **kwargs):
        return self.stream_json('stops_near', get_params)

    def get_stop(self, get_params, **kwargs):
        return self.stream_json('stop', get_params, "detailed")

    def get_stop_schedule(self, get_params, **kwargs):
        ret_val = self.stream_json('stop_schedule', get_params, "full")
        return ret_val

    def get_plan(self, get_params, **kwargs):
        return self.stream_json('plan_trip', get_params)

    def get_geocode(self, search):
        ret_val = None
        try:
            val = object_utils.to_url_param_val(search)
            ret_val = self.stream_json('geocode', "place={0}".format(val))
        except Exception as e:
            log.warning(e)
        return ret_val

    def get_atis_geocode(self, search):
        ret_val = None
        try:
            val = object_utils.to_url_param_val(search)
            ret_val = self.stream_json('atis_geocode', "place={0}".format(val))
        except Exception as e:
            log.warning(e)
        return ret_val


def main():
    m = Model()
    print(m.get_stop_schedule_single())
    print(m.get_stop_schedule_multiple())
    print(m.get_stop_schedule_by_time())
    routes=m.get_routes()['routes']
    for r in routes:
        print(r)


if __name__ == '__main__':
    main()
