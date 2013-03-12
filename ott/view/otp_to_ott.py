import simplejson as json
import logging
log = logging.getLogger(__file__)

class DateInfo(object):
    def __init__(self, jsn):
        pass

class Elevation(object):
    def __init__(self, jsn):
        pass


class Step(object):
    def __init__(self, jsn, name=None):
        self.alerts = None

class Route(object):
    def __init__(self, jsn):
        pass

class Fare(object):
    def __init__(self, jsn, name=None):
        pass

class Leg(object):
    def __init__(self, jsn, name=None):
        self.steps  = None
        self.alerts = None

class Stop(object):
    def __init__(self, jsn, name=None):
        # "stop": {"agencyId":"TriMet", "name":"SW Arthur & 1st", "id":"143","info":"stop.html?stop_id=143", "schedule":"stop_schedule.html?stop_id=143"},
        self.agency   = jsn['agencyId']
        self.name     = name
        self.id       = jsn['id']
        self.info     = self.make_info_url(id=self.id)
        self.schedule = self.make_schedule_url(id=self.id)

    def make_info_url(self, url="stop.html?stop_id=%(id)s", **kwargs):
        return url % kwargs

    def make_schedule_url(self, url="stop_schedule.html?stop_id=%(id)s", **kwargs):
        return url % kwargs

    @classmethod
    def factory(cls, jsn):
        if(jsn):
            if jsn:
                s = Stop(jsn)
                return s
        return None


class Place(object):
    def __init__(self, jsn, name=None):
        ''' '''
        self.name = jsn['name']
        self.lat  = jsn['lat']
        self.lon  = jsn['lon']
        self.stop = Stop.factory(jsn['stopId'])
        self.map_img = self.make_img_url(lon=self.lon, lat=self.lat, icon=self.map_icon(name))


    def map_icon(self, name):
        ''' '''
        ret_val = ''
        if name:
            x='/extraparams/format_options=layout:{0}'
            if name in ['from', 'end', 'last']:
                ret_val = x.format('end')
            elif name in ['to', 'start', 'begin']:
                ret_val = x.format('start')

        return ret_val


    def make_img_url(self, url="http://maps.trimet.org/eapi/ws/V1/mapimage/format/png/width/600/height/300/zoom/7/coord/%(lon)s,%(lat)s%(icon)s", **kwargs):
        return url % kwargs


    @classmethod
    def factory(cls, jsn, obj=None, name=None):
        ''' will create a Place object from json (jsn) data, 
            optionally assign the resultant object to some other object, as this alievates the akward 
            construct of 'from' that uses a python keyword, (e.g.,  self.__dict__['from'] = Place(j['from'])
        '''
        p = Place(jsn, name)
        if obj and name:
            obj.__dict__[name] = p

        return p


class Itinerary(object):
    def __init__(self, jsn):
        self.url = None
        self.selected = False
        self.transfers = -1
        self.legs = self.parse_legs(jsn['legs'])

    def parse_legs(self, legs):
        ret_val = []
        for l in legs:
            pass
        return ret_val

class Plan(object):
    ''' top level class of the ott 'plan' object tree

        contains these elements:
          self.from, self.to, self.params, self.arrive_by, self.optimize (plus other helpers 
    '''
    def __init__(self, jsn, params=None):
        # creates a self.from and self.to element in the Plan object
        Place.factory(jsn['from'], self, 'from')
        Place.factory(jsn['to'],   self, 'to')
        self.itineraries = []
        for i in jsn['itineraries']:
            itin = Itinerary(i)
            self.itineraries.append(itin)
        self.set_plan_params(params)

    def set_plan_params(self, params):
        ''' passed in by a separate routine, rather than parsed from returned itinerary
        '''
        # self.params = self.process_params(params)
        self.arrive_by = True   if params and 'arriveBy' in params and params['arriveBy'] else False
        self.optimize = "QUICK" if params is None or 'optimize' not in params else params['optimize']


def json_repr(obj):
    """ Represent instance of a class as JSON.
        returns a string that represents a JSON-encoded object.
        @from: http://stackoverflow.com/a/4682553/2125598
    """
    def serialize(obj):
        '''Recursively walk object's hierarchy.'''
        if(obj is None):
            return 'null'
        if isinstance(obj, (bool, int, long, float, basestring)):
            return obj
        elif isinstance(obj, dict):
            obj = obj.copy()
            for key in obj:
                obj[key.lower()] = serialize(obj[key])
            return obj
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(serialize([item for item in obj]))
        elif hasattr(obj, '__dict__'):
            return serialize(obj.__dict__)
        else:
            return repr(obj) # Don't know how to handle, convert to string
    return json.dumps(serialize(obj))


def main():
    #file='plan_walk.json'
    file='plan_transit.json'
    try:
        PATH='ott/view/static/test/'
        path="{0}{1}".format(PATH, file)
        f=open(path)
    except:
        PATH='static/test/'
        path="{0}{1}".format(PATH, file)
        f=open(path)

    j=json.load(f)
    p=Plan(j['plan'])
    print json_repr(p)

if __name__ == '__main__':
    main()
