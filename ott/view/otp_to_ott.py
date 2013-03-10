import simplejson as json
import logging
log = logging.getLogger(__file__)


class Stop(object):
    def __init__(self, jsn):
        # "stop": {"agencyId":"TriMet", "name":"SW Arthur & 1st", "id":"143","info":"stop.html?stop_id=143", "schedule":"stop_schedule.html?stop_id=143"},
        self.agency   = jsn['agencyId']
        self.name     = jsn['name']
        self.id       = jsn['id']
        self.info     = self.make_info_url(args=[self.id])
        self.schedule = self.make_schedule_url(args=[self.id])

    def make_info_url(self, url="stop.html?stop_id={}", *args):
        return url.format(args)

    def make_schedule_url(self, url="stop_schedule.html?stop_id={}", *args):
        return url.format(args)

    @classmethod
    def factory(cls, jsn):
        if(jsn):
            s = Stop(jsn)
            return s
        return None


class Place(object):
    def __init__(self, jsn, name=None):
        self.name = jsn['name']
        self.lat  = jsn['lat']
        self.lon  = jsn['lon']
        self.stop = Stop.factory(jsn['stopId'])
        self.map_img = self.make_img_url()

    def make_img_url(self, url="", *args):
        return url.format(args)

    @classmethod
    def factory(cls, jsn, obj=None, name=None):
        ''' will create a Place object from json (jsn) data, 
            optionally assign the resultant object to some other object, as this alievates the akward 
            construct of 'from' that uses a python keyword, (e.g.,  self.__dict__['from'] = Place(j['from'])
        '''
        p = Place(jsn)
        if obj and name:
            #p.stop = 
            obj.__dict__[name] = p
            
        return p


class Plan(object):
    def __init__(self, j):
        Place.factory(j['from'], self, 'from')
        Place.factory(j['to'],   self, 'to')


def json_repr(obj):
    """ Represent instance of a class as JSON.
        returns a string that reprent JSON-encoded object.
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
    PATH='ott/view/static/test/'
    file='plan_walk.json'
    path="{0}{1}".format(PATH, file)
    f=open(path)
    j=json.load(f)
    p=Plan(j['plan'])
    print json_repr(p)

if __name__ == '__main__':
    main()
