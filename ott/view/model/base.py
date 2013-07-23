import simplejson as json
import urllib
import logging
log = logging.getLogger(__file__)

class Base():

    TRAIN     = 'TRAIN'
    RAIL      = 'RAIL'
    STREETCAR = 'STREETCAR'
    TRAM      = 'TRAM'
    WALK      = 'WALK'
    GONDOLA   = 'GONDOLA'
    TRANSIT   = 'TRANSIT'
    BICYCLE   = 'BICYCLE'
    BIKE      =  BICYCLE


    def get_plan(self, get_params, **kwargs): pass

    def get_stop(self, get_params, **kwargs): pass
    def get_stop_schedule(self, get_params, **kwargs): pass

    def get_routes(self, get_params, **kwargs): pass
    def get_route_stops(self, get_params, **kwargs): pass

    def stream_json(self, u, args):
        ''' utility class to stream .json
        '''
        ret_val={}
        url = "{0}?{1}".format(u, args)
        stream = urllib.urlopen(url)
        otp = stream.read()
        ret_val = json.loads(otp)
        return ret_val

    def get_json(self, file, path='ott/view/static/test/'):
        ''' utility class to load a static .json file for mock'ing a service
        '''
        ret_val={}
        try:
            with open(file) as f:
                ret_val = json.load(f)
        except:
            try:
                path="{0}{1}".format(path, file)
                with open(path) as f:
                    ret_val = json.load(f)
            except:
                log.info("Couldn't open file : {0} (or {1})".format(file, path))

        return ret_val

