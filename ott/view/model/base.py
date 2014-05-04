import simplejson as json
import urllib
import re
import logging
log = logging.getLogger(__file__)

from ott.view.utils import config
from ott.view.utils import object_utils

class Base(object):
    def __init__(self):
        self.service_cache = {}

    def get_plan(self, get_params, **kwargs): pass

    def get_geocode(self, get_params, **kwargs): pass

    def get_stop(self, get_params, **kwargs): pass
    def get_stop_schedule(self, get_params, **kwargs): pass
    def get_stops_near(self, get_params, **kwargs): pass

    def get_routes(self, get_params, **kwargs): pass
    def get_route_stops(self, get_params, **kwargs): pass

    def get_adverts(self, get_params, **kwargs): pass

    def _cache_svc_url(self, svc):
        ret_val = svc
        if svc in self.service_cache:
            ret_val = self.service_cache[svc]
        else:
            domain = config.get('controller', 'http://127.0.0.1:44444')
            url = "{0}/{1}".format(domain, svc)
            url = re.sub(r"/+", "/", url)     # get rid of extra /, ala http://x/y//z///b
            url = url.replace(":/", "://")    # fix http:// part from line above...
            url = urllib.quote_plus(url, safe="%/:=&?~#+!$,;'@()*[]")
            self.service_cache[svc] = url
            ret_val = url
        return ret_val

    def get_service_url(self, svc, args):
        #import pdb; pdb.set_trace()
        url = self._cache_svc_url(svc)
        url = "{0}?{1}".format(url, object_utils.to_str(args))
        '''
            TODO : IDEA
            
            PROBLEM: we might want to CACHE the return from the service
                     problem is, the url to the the service might contain params that
                     defeat caching
            
            Since a lot of pages will send down 'all' their params (in
            
        '''


        return url

    def stream_json(self, svc, args):
        ''' utility class to stream .json
        '''
        ret_val={}
        url = self.get_service_url(svc, args)
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

