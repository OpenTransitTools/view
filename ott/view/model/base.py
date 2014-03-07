import simplejson as json
import urllib
import logging
log = logging.getLogger(__file__)

from ott.view.utils import config
from ott.view.utils import object_utils

class Base(object):

    def get_plan(self, get_params, **kwargs): pass

    def get_geocode(self, get_params, **kwargs): pass

    def get_stop(self, get_params, **kwargs): pass
    def get_stop_schedule(self, get_params, **kwargs): pass
    def get_stops_near(self, get_params, **kwargs): pass

    def get_routes(self, get_params, **kwargs): pass
    def get_route_stops(self, get_params, **kwargs): pass

    def get_adverts(self, get_params, **kwargs): pass

    def stream_json(self, svc, args):
        ''' utility class to stream .json
        '''
        ret_val={}
        #import pdb; pdb.set_trace()
        domain = config.get('controller', 'http://127.0.0.1:34443')
        url = "{0}/{1}?{2}".format(domain, svc, object_utils.to_str(args))
        log.info("calling service: {0}".format(url))
        stream = urllib.urlopen(url)
        otp = stream.read()
        ret_val = json.loads(otp)
        return ret_val

    def get_json(self, file, path='ott/view/static/mock/'):
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

