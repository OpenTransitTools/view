import simplejson as json
import logging
log = logging.getLogger(__file__)


class Model():

    TRAIN   = 'TRAIN'
    WALK    = 'WALK'
    TRANSIT = 'TRANSIT'
    BICYCLE = 'BICYCLE'
    BIKE    =  BICYCLE

    def get_routes(self): pass
    def get_plans(self, **kwargs): pass

def main():
    m=Model()
    r=m.get_routes()
    print r


if __name__ == '__main__':
    main()
