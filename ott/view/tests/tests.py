import os
import sys
import unittest
import urllib
import contextlib

from ott.utils import config_util
from ott.utils import file_utils


class OttTestCase(unittest.TestCase):
    domain = "localhost"
    port = "33333"
    path = None
    url_file = None

    def get_url(self, svc_name, params=None, lang=None):
        # import pdb; pdb.set_trace()
        if self.path:
            ret_val = "http://{}:{}/{}/{}".format(self.domain, self.port, self.path, svc_name)
        else:
            ret_val = "http://{}:{}/{}".format(self.domain, self.port, svc_name)
        if params:
            ret_val = "{0}?{1}".format(ret_val, params)
        if lang:
            ret_val = "{0}&_LOCALE_={1}".format(ret_val, lang)
        if self.url_file:
            url = ret_val.replace(" ", "+")
            self.url_file.write(url)
            self.url_file.write("\n")
        return ret_val

    def call_url(self, url):
        ret_json = None
        with contextlib.closing(urllib.urlopen(url)) as f:
            ret_json = f.read()
        return ret_json

    def setUp(self):
        dir = file_utils.get_project_root_dir()
        ini = config_util.ConfigUtil('development.ini', run_dir=dir)

        port = ini.get('ott.test_port', 'app:main')
        if not port:
            port = ini.get('ott.svr_port', 'app:main', self.port)
        self.port = port

        url_file = ini.get('ott.test_urlfile', 'app:main')
        if url_file:
            self.url_file = open(os.path.join(dir, url_file), "a+")

        test_domain = ini.get('ott.test_domain', 'app:main')
        if test_domain:
            self.domain = test_domain

        test_path = ini.get('ott.test_path', 'app:main')
        if test_path:
            self.path = test_path

    def tearDown(self):
        if self.url_file:
            url_file.flush()
            url_file.close()

    def call_url_match_list(self, url, list):
        u = self.call_url(url)
        for l in list:
            self.assertRegexpMatches(u, l)

    def call_url_match_string(self, url, str):
        u = self.call_url(url)
        self.assertRegexpMatches(u, str)


class ViewTests(OttTestCase):

    def test_stops_near(self):
        for m in ['', 'm/']:
            ''' '''
            # test place and placeCoord
            url = self.get_url(m + 'stops_near.html', 'placeCoord=45.5,-122.5&place=XTCvsAdamAnt')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"miles away")
            self.assertRegexpMatches(s,"SE Division")
            self.assertRegexpMatches(s,"XTCvsAdamAnt")

            # test named coord
            url = self.get_url(m + 'stops_near.html', 'place=834 SE LAMBERT ST::45.468602,-122.657627')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"miles away")

            # test named coord w/ city
            url = self.get_url(m + 'stops_near.html', 'place=834 SE LAMBERT ST::45.468602,-122.657627::Portland')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "miles away")

            # test place as just a coord
            url = self.get_url(m + 'stops_near.html', 'place=45.468602,-122.65762')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "miles away")

            # test place as just a coord
            url = self.get_url(m + 'stops_near.html', 'place=Stop ID 2')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "A Ave &amp; Chandler")

            # test interpolated address
            url = self.get_url(m + 'stops_near.html', 'place=888 Lambert St&show_more=true')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "Tacoma")

            # test known address from MA file
            url = self.get_url(m + 'stops_near.html', 'place=834 Lambert St&show_more=true')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "Tacoma")

            # test ambiguous address from interpolated system...
            url = self.get_url(m + 'stops_near.html', 'place=834 Lambert&show_more=true')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "Uncertain location")
            self.assertRegexpMatches(s, "834 SE LAMBERT CIRCLE")
            self.assertRegexpMatches(s, "834 SE LAMBERT ST")

    def test_stop_select_form(self):
        ''' routes ws: list of route '''
        for m in ['', 'm/']:
            url = self.get_url(m + 'stop_select_form.html')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"MAX Blue")

    def test_stop_select_list(self):
        ''' route stops ws: stop select for each route direction '''
        for m in ['', 'm/']:
            url = self.get_url(m + 'stop_select_list.html', 'route=100')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"MAX Blue")
            self.assertRegexpMatches(s,"Hatfield")

    def test_stop(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'stop.html', 'stop_id=2')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"Lake Oswego")

    def test_localization(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'stop.html', 'stop_id=2&_LOCALE_=es')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"Lake Oswego")

    def test_stop_schedule(self):
        for m in ['', 'm/']:
            for t in ['&sort=destination', '&sort=time']:
                url = self.get_url(m + 'stop_schedule.html', 'stop_id=2' + t)
                s = self.call_url(url)
                self.assertRegexpMatches(s,"Lake Oswego")

                url = self.get_url(m + 'stop_schedule.html', 'stop_id=2&more' + t)
                s = self.call_url(url)
                self.assertRegexpMatches(s,"Lake Oswego")

    def test_plan_form(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'planner_form.html', 'from=PDX::45.587546,-122.592925&to=ZOO')
            s = self.call_url(url)
            self.assertRegexpMatches(s, 'type="text" id="from" name="from" value="PDX"')
            self.assertRegexpMatches(s, 'type="text" id="going" name="to" value="ZOO"')

    def test_plan_trip(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'planner.html', 'to=pdx::45.587546,-122.592925&from=zoo::45.5092,-122.7133&Hour=9&Minute=0&AmPm=pm')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"MAX Red Line")

    def test_plan_walk(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'planner_walk.html', 'mode=WALK&from=pdx::45.587546,-122.592925&to=zoo')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"Airport Way")

    def test_map_place(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'map_place.html', 'name=834 SE MILL ST&city=Portland&lon=-122.65705&lat=45.509865')
            s = self.call_url(url)
            self.assertRegexpMatches(s,"Plan a trip to 834 SE MILL ST")
            self.assertRegexpMatches(s,"ride.trimet.org")


class GeoCoderTests(OttTestCase):
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
                    url = self.get_url(m + 'stops_near.html', 'place=' + p, l)
                    self.call_url_match_list(url, "stopimage/format/png/width/340/height/300/zoom/6")

    def test_stops_near_geocode_route_stops(self):
        for l in [None, 'es']:
            for m in ['', 'm/']:
                for s in self.route_stops:
                    url = self.get_url(m + 'stops_near.html', 'place=' + s[0], l)
                    self.call_url_match_list(url, s[1])

    def test_stops_near_geocode(self):
        for l in [None, 'es']:
            for m in ['', 'm/']:
                for s in self.stops:
                    url = self.get_url(m + 'stops_near.html', 'place=' + s[0], l)
                    self.call_url_match_string(url, s[1])

    def test_not_found_geocode(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'stops_near.html', 'place=' + '8444455  ddaxxxdfas asdfasfas')
            self.call_url_match_string(url, 'We cannot find')

    def test_not_found_geocode_es(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'stops_near.html', 'place=' + '8444455  ddaxxxdfas asdfasfas', 'es')
            self.call_url_match_string(url, 'Lugar indefinido')

    def test_geocode(self):
        for l in [None, 'es']:
            for m in ['', 'm/']:
                url = self.get_url(m + 'planner.html', 'from=834 XX Portland', l)
                self.call_url_match_list(url, ["834 SE MILL", "834 SE LAMBERT"])

