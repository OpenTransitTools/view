import os
import sys
import unittest
import urllib
import contextlib

from ott.utils import config_util
from ott.utils import file_utils

PORT = "33333"
DOMAIN = "localhost"
URL_FILE = None

def set_port(port):
    global PORT
    PORT = port


def get_url(svc_name, params=None, lang=None):
    ret_val = "http://{}:{}/{}".format(DOMAIN, PORT, svc_name)
    if params:
        ret_val = "{0}?{1}".format(ret_val, params)
    if lang:
        ret_val = "{0}&_LOCALE_={1}".format(ret_val, lang)
    if URL_FILE:
        URL_FILE.write(ret_val)
    return ret_val


def call_url(url):
    ret_json = None
    with contextlib.closing(urllib.urlopen(url)) as f:
        ret_json = f.read()
    return ret_json


class MyTestCase(unittest.TestCase):
    def setUp(self):
        #import pdb; pdb.set_trace()
        dir = file_utils.get_project_root_dir()
        ini = config_util.ConfigUtil('development.ini', run_dir=dir)
        port = ini.get('ott.svr_port', 'app:main', PORT)
        set_port(port)

        global URL_FILE
        URL_FILE = open(os.path.join(dir, "urlfile.txt"), 'w+')

    def tearDown(self):
        if URL_FILE:
            URL_FILE.close()

    def call_url_match_list(self, url, list):
        u = call_url(url)
        for l in list:
            self.assertRegexpMatches(u, l)

    def call_url_match_string(self, url, str):
        u = call_url(url)
        self.assertRegexpMatches(u, str)


class ViewTests(MyTestCase):

    def test_stops_near(self):
        for m in ['', 'm/']:
            ''' '''
            # test place and placeCoord
            url = get_url(m + 'stops_near.html', 'placeCoord=45.5,-122.5&place=XTCvsAdamAnt')
            s = call_url(url)
            self.assertRegexpMatches(s,"miles away")
            self.assertRegexpMatches(s,"SE Division")
            self.assertRegexpMatches(s,"XTCvsAdamAnt")

            # test named coord
            url = get_url(m + 'stops_near.html', 'place=834 SE LAMBERT ST::45.468602,-122.657627')
            s = call_url(url)
            self.assertRegexpMatches(s,"miles away")

            # test named coord w/ city
            url = get_url(m + 'stops_near.html', 'place=834 SE LAMBERT ST::45.468602,-122.657627::Portland')
            s = call_url(url)
            self.assertRegexpMatches(s, "miles away")

            # test place as just a coord
            url = get_url(m + 'stops_near.html', 'place=45.468602,-122.65762')
            s = call_url(url)
            self.assertRegexpMatches(s, "miles away")

            # test place as just a coord
            url = get_url(m + 'stops_near.html', 'place=Stop ID 2')
            s = call_url(url)
            self.assertRegexpMatches(s, "A Ave &amp; Chandler")

            # test interpolated address
            url = get_url(m + 'stops_near.html', 'place=888 Lambert St&show_more=true')
            s = call_url(url)
            self.assertRegexpMatches(s, "Tacoma")

            # test known address from MA file
            url = get_url(m + 'stops_near.html', 'place=834 Lambert St&show_more=true')
            s = call_url(url)
            self.assertRegexpMatches(s, "Tacoma")

            # test ambiguous address from interpolated system...
            url = get_url(m + 'stops_near.html', 'place=834 Lambert&show_more=true')
            s = call_url(url)
            self.assertRegexpMatches(s, "Uncertain location")
            self.assertRegexpMatches(s, "834 SE LAMBERT CIRCLE")
            self.assertRegexpMatches(s, "834 SE LAMBERT ST")

    def test_stop_select_form(self):
        ''' routes ws: list of route '''
        for m in ['', 'm/']:
            url = get_url(m + 'stop_select_form.html')
            s = call_url(url)
            self.assertRegexpMatches(s,"MAX Blue")

    def test_stop_select_list(self):
        ''' route stops ws: stop select for each route direction '''
        for m in ['', 'm/']:
            url = get_url(m + 'stop_select_list.html', 'route=100')
            s = call_url(url)
            self.assertRegexpMatches(s,"MAX Blue")
            self.assertRegexpMatches(s,"Hatfield")

    def test_stop(self):
        for m in ['', 'm/']:
            url = get_url(m + 'stop.html', 'stop_id=2')
            s = call_url(url)
            self.assertRegexpMatches(s,"Lake Oswego")

    def test_localization(self):
        for m in ['', 'm/']:
            url = get_url(m + 'stop.html', 'stop_id=2&_LOCALE_=es')
            s = call_url(url)
            self.assertRegexpMatches(s,"Lake Oswego")

    def test_stop_schedule(self):
        for m in ['', 'm/']:
            for t in ['&sort=destination', '&sort=time']:
                url = get_url(m + 'stop_schedule.html', 'stop_id=2' + t)
                s = call_url(url)
                self.assertRegexpMatches(s,"Lake Oswego")

                url = get_url(m + 'stop_schedule.html', 'stop_id=2&more' + t)
                s = call_url(url)
                self.assertRegexpMatches(s,"Lake Oswego")

    def test_plan_form(self):
        for m in ['', 'm/']:
            url = get_url(m + 'planner_form.html', 'from=PDX::45.587546,-122.592925&to=ZOO')
            s = call_url(url)
            self.assertRegexpMatches(s, 'type="text" id="from" name="from" value="PDX"')
            self.assertRegexpMatches(s, 'type="text" id="going" name="to" value="ZOO"')

    def test_plan_trip(self):
        for m in ['', 'm/']:
            url = get_url(m + 'planner.html', 'to=pdx::45.587546,-122.592925&from=zoo::45.5092,-122.7133&Hour=9&Minute=0&AmPm=pm')
            s = call_url(url)
            self.assertRegexpMatches(s,"MAX Red Line")

    def test_plan_walk(self):
        for m in ['', 'm/']:
            url = get_url(m + 'planner_walk.html', 'mode=WALK&from=pdx::45.587546,-122.592925&to=zoo')
            s = call_url(url)
            self.assertRegexpMatches(s,"Airport Way")

    def test_map_place(self):
        for m in ['', 'm/']:
            url = get_url(m + 'map_place.html', 'name=834 SE MILL ST&city=Portland&lon=-122.65705&lat=45.509865')
            s = call_url(url)
            self.assertRegexpMatches(s,"Plan a trip to 834 SE MILL ST")
            self.assertRegexpMatches(s,"ride.trimet.org")


#class DontRunTests():
class GeoCoderTests(MyTestCase):
    stops = [
        ['834',   '834 SE LAMBERT ST'],
        ['2',     'A Ave &amp; Chandler'],
        ['10093', 'NW Bethany &amp; Laidlaw'],
        ['10092', '4700 Block NW Bethany'],
        ['10108', '4700 Block NW Bethany'],
        ['10107', 'NW Bethany &amp; Laidlaw'],
        ['10114', 'NW Bethany &amp; Oak Hills Dr'],
        ['8920',  'SW Walker &amp; Butner'],
        ['5590',  'SW Tualatin Valley Hwy &amp; Market Centre'],
        ['10111', 'NW Bethany &amp; West Union'],
        ['10089', 'NW Bethany &amp; West Union'],
        ['13685', 'NW Laidlaw &amp; Bethany'],
        ['6830',  'SW 158th &amp; Jay']
    ]

    route_stops = [
        ['929',  ['044', '054', '056'] ],
    ]

    def test_stops_near_stop_id(self):
        ''' check that the following place queries hit a stop page (via the stop image url)
        '''
        places = [
            "2",
            "A+Ave+Chandler+Lake+Oswego+(Stop+ID+2)",
            "Stop ID 8",
        ]
        for l in [None, 'es']:
            for m in ['', 'm/']:
                for p in places:
                    url = get_url(m + 'stops_near.html', 'place=' + p, l)
                    self.call_url_match_list(url, "stopimage/format/png/width/340/height/300/zoom/6")

    def test_stops_near_geocode_route_stops(self):
        for l in [None, 'es']:
            for m in ['', 'm/']:
                for s in self.route_stops:
                    url = get_url(m + 'stops_near.html', 'place=' + s[0], l)
                    self.call_url_match_list(url, s[1])

    def test_stops_near_geocode(self):
        for l in [None, 'es']:
            for m in ['', 'm/']:
                for s in self.stops:
                    url = get_url(m + 'stops_near.html', 'place=' + s[0], l)
                    self.call_url_match_string(url, s[1])

    def test_not_found_geocode(self):
        for m in ['', 'm/']:
            for s in self.stops:
                url = get_url(m + 'stops_near.html', 'place=' + '8444455  ddaxxxdfas asdfasfas')
                self.call_url_match_string(url, 'We cannot find')

    def test_not_found_geocode_es(self):
        for m in ['', 'm/']:
            for s in self.stops:
                url = get_url(m + 'stops_near.html', 'place=' + '8444455  ddaxxxdfas asdfasfas', 'es')
                self.call_url_match_string(url, 'Lugar indefinido')

    def test_geocode(self):
        for l in [None, 'es']:
            for m in ['', 'm/']:
                url = get_url(m + 'planner.html', 'from=834 XX Portland', l)
                self.call_url_match_list(url, ["834 SE MILL", "834 SE LAMBERT"])

