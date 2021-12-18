import os
import re
import requests
from ott.utils import object_utils

import logging
log = logging.getLogger(__file__)


class Base(object):
    def __init__(self, services_domain=None, map_url=None):
        # import pdb; pdb.set_trace()
        self.service_cache = {}
        self.services_domain = services_domain if services_domain else "http://localhost:44444"
        self.map_url = map_url if map_url else "http://ride.trimet.org"

    def get_plan(self, get_params, **kwargs): pass

    def get_geocode(self, get_params, **kwargs): pass
    def get_atis_geocode(self, get_params, **kwargs): pass

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
            url = "{0}/{1}".format(self.services_domain, svc)
            url = re.sub(r"/+", "/", url)     # get rid of extra /, ala http://x/y//z///b
            url = url.replace(":/", "://")    # fix http:// part from line above...
            #url = urllib.quote_plus(url, safe="%/:=?&~#+!$,;'@()*[]")
            self.service_cache[svc] = url
            ret_val = url
        return ret_val

    def get_service_url(self, svc, args):
        url = self._cache_svc_url(svc)
        url = "{0}?{1}".format(url, object_utils.to_str(args))
        return url

    def stream_json(self, svc, args, extra=None):
        """ utility class to stream .json
        """
        ret_val = {}
        url = self.get_service_url(svc, args)
        if extra:
            url = url + "&" + extra
        try:
            log.info("calling service: {0}".format(url))
            ret_val = requests.get(url).json()
        except Exception as e:
            log.error(e)
        return ret_val

    def get_json(self, file, path='ott/view/static/mock/'):
        """ utility class to load a static .json file for mock'ing a service
        """
        import simplejson as json
        ret_val={}
        try:
            with open(file) as f:
                ret_val = json.load(f)
        except Exception as e:
            try:
                path = os.path.join(path, file)
                with open(path) as f:
                    ret_val = json.load(f)
            except Exception as e:
                log.info("Couldn't open file : {0} (or {1})".format(file, path))
        return ret_val
