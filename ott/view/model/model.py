import simplejson as json
import logging
log = logging.getLogger(__file__)

from ott.view.model.base import Base

class Model(Base):

    def get_routes(self): pass
    def get_plan(self, get_params, **kwargs): pass


def main():
    m=Model()
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
