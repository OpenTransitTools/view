import sys
import math
from decimal import *
from fractions import Fraction
import datetime
import simplejson as json
import logging
log = logging.getLogger(__file__)

class DateInfo(object):
    def __init__(self, jsn):
        self.start_time_ms = jsn['startTime']
        self.end_time_ms = jsn['endTime']
        start = datetime.datetime.fromtimestamp(self.start_time_ms / 1000)
        end   = datetime.datetime.fromtimestamp(self.end_time_ms / 1000)

        self.date = "%d/%d/%d" % (start.month, start.day, start.year) # 29/2/2012
        self.pretty_date = start.strftime("%A, %B %d, %Y").replace(' 0',' ')    # "Monday, March 4, 2013"
        self.start_time  = start.strftime(" %I:%M%p").lower().replace(' 0','') # "3:40pm"
        self.end_time = end.strftime(" %I:%M%p").lower().replace(' 0','')    # "3:44pm"
        self.duration_ms = jsn['duration']
        self.duration = ms_to_minutes(self.duration_ms, is_pretty=True, show_hours=True)


class DateInfoExtended(DateInfo):
    '''
    '''
    def __init__(self, jsn):
        super(DateInfoExtended, self).__init__(jsn)
        self.extended = True

        # step 1: get data
        walk = get_element(jsn, 'walkTime', 0)
        tran = get_element(jsn, 'transitTime', 0)
        wait = get_element(jsn, 'waitingTime', 0)
        tot  = walk + tran + wait

        # step 2: trip length
        h,m = seconds_to_hours_minutes(tot)
        self.total_time_hours = h
        self.total_time_mins = m

        # step 3: transit info
        h,m = seconds_to_hours_minutes(tran)
        self.transit_time_hours = h
        self.transit_time_mins = m
        self.start_transit = "TODO"
        self.end_transit = "TODO"

        # step 4: bike / walk length
        self.bike_time_hours = None
        self.bike_time_mins = None
        self.walk_time_hours = None
        self.walk_time_mins = None
        if 'mode' in jsn and jsn['mode'] == 'BICYCLE':
            h,m = seconds_to_hours_minutes(walk)
            self.bike_time_hours = h
            self.bike_time_mins = m
        else:
            h,m = seconds_to_hours_minutes(walk)
            self.walk_time_hours = h
            self.walk_time_mins = m

        # step 5: wait time
        h,m = seconds_to_hours_minutes(wait)
        self.wait_time_hours = h
        self.wait_time_mins = m

        # step 5: drive time...unused as of now...
        self.drive_time_hours = None
        self.drive_time_mins = None

        self.text = self.get_text()

    def get_text(self):
        '''
        '''
        ret_val = ''
        tot =  hour_min_string(self.total_time_hours, self.total_time_mins)
        walk = hour_min_string(self.walk_time_hours, self.walk_time_mins)
        bike = hour_min_string(self.bike_time_hours, self.bike_time_mins)
        wait = hour_min_string(self.wait_time_hours, self.wait_time_mins)
        return ret_val


class Elevation(object):
    def __init__(self, jsn):
        self.points = "190.4,189.5,189.1,188.5,188.1,187.5,187.2,187.2"
        self.high = "190.4"
        self.low  = "187.2"
        self.distance = "1111111" # could be walk / bike


class Route(object):
    def __init__(self, jsn):
        self.agency_id = jsn['agencyId']
        self.agency_name = get_element(jsn, 'agencyName')
        self.id = jsn['routeId']
        self.name = self.make_name(jsn)
        self.headsign = get_element(jsn, 'headsign')
        self.trip = get_element(jsn, 'tripId')
        self.url = None
        if self.agency_id == 'TriMet':
            self.url = "http://trimet.org/schedules/r{0}.htm".format(self.id.zfill(3))
        elif self.agency_id == 'C-TRAN':
            self.url = "http://c-tran.com/routes/{0}route/index.html".format(self.id)

    def make_name(self, jsn, name_sep='-'):
        ret_val = None
        sn = jsn['routeShortName']
        ln = jsn['routeLongName']
        if sn and len(sn) > 0:
            ret_val = sn
        if ln and len(ln) > 0:
            if ret_val and name_sep:
                ret_val = ret_val + name_sep
            else: 
                ret_val = ''
            ret_val = ret_val + ln
        return ret_val


class Fare(object):
    '''
    '''
    def __init__(self, jsn):
        self.adult       = self.get_fare(jsn, '$2.50')
        self.adult_day   = "$5.00"
        self.honored     = "$1.00"
        self.honored_day = "$2.00"
        self.youth       = "$1.65"
        self.youth_day   = "$3.30"
        self.tram        = "$4.00"

    def get_fare(self, jsn, def_val):
        ret_val = def_val
        try:
            c = int(jsn['fare']['fare']['regular']['cents']) * 0.01
            s = jsn['fare']['fare']['regular']['currency']['symbol']
            ret_val = "%s%.2f" % (s, c)
        except Exception, e:
            pass
        return ret_val


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
        self.map_img = self.make_img_url(lon=self.lon, lat=self.lat, icon=self.endpoint_icon(name))

    def endpoint_icon(self, name):
        ''' '''
        ret_val = ''
        if name:
            x='/extraparams/format_options=layout:{0}'
            if name in ['to', 'end', 'last']:
                ret_val = x.format('end')
            elif name in ['from', 'start', 'begin']:
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


class Step(object):
    def __init__(self, jsn):
        self.name = jsn['streetName']
        self.lat  = jsn['lat']
        self.lon  = jsn['lon']
        self.distance_feet  = jsn['distance']
        self.distance = pretty_distance(self.distance_feet)
        self.elevation = jsn['elevation']
        self.compass_direction = self.get_direction(jsn['absoluteDirection'])
        self.relative_direction = self.get_direction(jsn['relativeDirection'])
        self.alerts = None

    @classmethod
    def get_direction(cls, dir):
        ''' TODO localize me 
        '''
        ret_val = dir
        try:
            ret_val = {
                'LEFT' : dir.lower(),
                'RIGHT': dir.lower(),
                'CONTINUE': dir.lower(),

                'NORTH': dir.lower(),
                'SOUTH': dir.lower(),
                'EAST': dir.lower(),
                'WEST': dir.lower(),
                'NORTHEAST': dir.lower(),
                'NORTHWEST': dir.lower(),
                'SOUTHEAST': dir.lower(),
                'SOUTHWEST': dir.lower(),
            }[dir]
        except:
            pass

        return ret_val

    @classmethod
    def get_relative_direction(cls, dir):
        ''' '''
        ret_val = dir
        return ret_val


class Leg(object):
    '''
    '''
    def __init__(self, jsn):
        self.mode = jsn['mode']

        Place.factory(jsn['from'], self, 'from')
        Place.factory(jsn['to'],   self, 'to')

        self.elevation = Elevation(jsn)
        self.date_info = DateInfo(jsn)

        self.route = None
        self.steps = self.get_steps(jsn)
        self.alerts = None
        self.transfer = None
        self.interline = None
        self.compass_direction = self.get_compass_direction()
        self.distance_feet = jsn['distance']
        self.distance = pretty_distance(self.distance_feet)

        # mode specific config
        if self.is_transit_mode():
            self.route = Route(jsn)
            self.interline = jsn['interlineWithPreviousLeg']

    def is_transit_mode(self):
        return self.mode in ['BUS', 'TRAM', '... TODO is_transit_mode() ... ']

    def is_walk_or_bike_mode(self):
        return self.mode in ['BIKE', 'WALK', '... TODO is_X_mode() ... ']

    def get_steps(self, jsn):
        ret_val = None
        if 'steps' in jsn and len(jsn['steps']) > 0:
            ret_val = []
            for s in jsn['steps']:
                step = Step(s)
                ret_val.append(step)

        return ret_val

    def get_compass_direction(self):
        ret_val = None
        if self.steps and len(self.steps) > 0:
            v = self.steps[0].compass_direction
            if v:
                ret_val = v

        return ret_val


class Itinerary(object):
    '''
    '''
    def __init__(self, jsn):
        self.elevation = Elevation(jsn)
        self.fare = Fare(jsn)
        self.url = None
        self.selected = False
        self.transfers = jsn['transfers']
        self.date_info = DateInfoExtended(jsn)
        self.elevation = Elevation(jsn)
        self.legs = self.parse_legs(jsn['legs'])

    def parse_legs(self, legs):
        ''' '''
        ret_val = []

        # step 1: build the legs
        for l in legs:
            leg = Leg(l)
            ret_val.append(leg)

        # step 2: find transfer legs e.g., this pattern TRANSIT LEG, WALK/BIKE LEG, TRANSIT LEG
        for i, leg in enumerate(ret_val):
            if leg.is_transit_mode() and i+2 > len(ret_val): 
                if ret_val[i+2].is_transit_mode() and ret_val[i+1].is_walk_or_bike_mode():
                    self.transfer = True

        return ret_val


class Plan(object):
    ''' top level class of the ott 'plan' object tree

        contains these elements:
          self.from, self.to, self.params, self.arrive_by, self.optimize (plus other helpers 
    '''
    def __init__(self, jsn, params=None):
        ''' creates a self.from and self.to element in the Plan object '''
        Place.factory(jsn['from'], self, 'from')
        Place.factory(jsn['to'],   self, 'to')
        self.itineraries = self.parse_itineraries(jsn['itineraries'], params)
        self.set_plan_params(params)


    def parse_itineraries(self, itineraries, params):
        '''  
        '''
        ret_val = []
        for i in itineraries:
            itin = Itinerary(i)
            ret_val.append(itin)

        # set the selected 
        selected = self.get_selected_itinerary(params, len(ret_val))
        if selected < len(ret_val):
            ret_val[selected].selected = True

        return ret_val


    def get_selected_itinerary(self, params, max=3):
        ''' return list position (index starts at zero) of the 'selected' itinerary '''
        ret_val = 0
        if params and 'selected' in params:
            try:
                ret_val = int(params['selected'])
            except: 
                log.info("params['selected'] has a value of {0}".format(params['selected']))

        # final check to make sure we don't over-index the list of itineraries
        if ret_val < 0 or ret_val >= max:
            ret_val = 0

        return ret_val

    def set_plan_params(self, params):
        ''' passed in by a separate routine, rather than parsed from returned itinerary
        '''
        # self.params = self.process_params(params)
        self.arrive_by = True   if params and 'arriveBy' in params and params['arriveBy'] else False
        self.optimize = "QUICK" if params is None or 'optimize' not in params else params['optimize']
        self.params  = 'TODO TODO TODO'


'''
UTILITY METHODS
'''
def get_element(jsn, name, def_val=None):
    '''
    '''
    ret_val = def_val
    try:
        v = jsn[name]
        if type(def_val) == int:
            ret_val = int(v)
        else:
            ret_val = v
    except:
        log.debug(name + " not an int value in jsn")
    return ret_val


def ms_to_minutes(ms, is_pretty=False, show_hours=False):
    ret_val = ms / 1000 / 60

    # pretty '3 hours & 1 minute' string
    if is_pretty:
        h_str = ''
        m_str = ''

        # calculate hours string
        m = ret_val
        if show_hours and m > 60:
            h = int(floor(m / 60))
            m = int(m % 60)
            if h > 0:
                hrs =  'hour' if h == 1 else 'hours'
                h_str = '%d %s' % (h, hrs)
                if m > 0:
                    h_str = h_str + ' ' + '&' + ' '

        # calculate minutes string
        if m > 0:
            mins = 'minute' if m == 1 else 'minutes'
            m_str = '%d %s' % (m, mins)

        ret_val = '%s%s' % (h_str, m_str) 

    return ret_val


def hour_min_string(h, m, fmt='{0} {1}', sp=', '):
    ret_val = None
    if h and h > 0:
        hr = 'hours' if h > 1 else 'hour'
        ret_val = "{0} {1}".format(h, hr)
    if m:
        min = 'minutes' if m > 1 else 'minute'
        pre = '' if ret_val == None else ret_val + sp 
        ret_val = "{0}{1} {2}".format(pre, m, min)
    return ret_val


def seconds_to_hours_minutes(secs, def_val=None, min_secs=60):
    '''
    '''
    min = def_val
    hour = def_val
    if(secs > min_secs):
        m = math.floor(secs / 60)
        min  = m % 60
        if m >= 60:
            m = m - min
            hour = int(math.floor(m / 60))
    return hour,min


def pretty_distance(feet, def_val=None, min_distance=550, denominator=10):
    '''
    '''
    ret_val = def_val

    if min_distance > 0 and def_val is None and feet < min_distance:
        #import pdb; pdb.set_trace()
        feet = min_distance

    m = int(math.floor(feet / 5280.0))
    n = (feet % 5280) / 5280.0
    f = Fraction(str(n)).limit_denominator(denominator)

    r = ''
    if m > 0 and f > 0:
        ret_val = '{0} {1} {2}'.format(m, f, 'miles')
    elif m > 1: 
        ret_val = '{0} {1}'.format(m, 'miles')
    elif m == 1 or f > 0:
        ret_val = '{0} {1}'.format(f if f > 0 else m, 'mile')

    return ret_val


def json_repr(obj, pretty_print=False):
    """ Represent instance of a class as JSON.
        returns a string that represents a JSON-encoded object.
        @from: http://stackoverflow.com/a/4682553/2125598
    """
    def serialize(obj):
        '''Recursively walk object's hierarchy.'''
        if(obj is None):
            return None
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


    ## step 1: call serializer, which walks object tree and returns a cleaned up dict representation of the object
    output = serialize(obj)

    ## step 2: dump serialized object into json string
    ret_val = None
    if pretty_print:
        ret_val = json.dumps(output, sort_keys=True, indent=4)
    else:
        ret_val = json.dumps(output)

    ## step 3: return result
    return ret_val


def main(argv):
    #file='plan_walk.json'
    file='plan_raw_pdx-zoo.json'
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
    pretty = 'pretty' in argv
    y = json_repr(p, pretty)
    z = json.loads(y)
    print y
    #print z

if __name__ == '__main__':
    main(sys.argv)
