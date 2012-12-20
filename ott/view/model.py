import simplejson as json
import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)


class Model():
    def get_routes(self):
        pass

def main():
    m=Model()
    r=m.get_routes()
    print r


if __name__ == '__main__':
    main()
