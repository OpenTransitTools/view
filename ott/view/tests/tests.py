import unittest
from pyramid import testing

import urllib
import contextlib
import json
import re

PORT="33333"

class MyTestCase(unittest.TestCase):
    def call_url_match_list(self, url, list):
        u = call_url(url)
        for l in list:
            self.assertRegexpMatches(u, l)
    
    def call_url_match_string(self, url, str):
        u = call_url(url)
        self.assertRegexpMatches(u, str)

def get_url(svc_name, params=None):
    ret_val = "http://localhost:{0}/{1}".format(PORT, svc_name)
    if params:
        ret_val = "{0}?{1}".format(ret_val, params)
    return ret_val

def call_url(url):
    ret_json = None
    with contextlib.closing(urllib.urlopen(url)) as f:
        ret_json = f.read()
    return ret_json


class GeoCoderTests(MyTestCase):
    stops = [
            ['834',   '834 SE LAMBERT ST'],
            ['2',     'A Ave &amp; Chandler Eastbound'],
            ['10093', 'NW Bethany &amp; Laidlaw Northbound'],
            ['10092', '4700 Block NW Bethany Northbound'],
            ['10108', '4700 Block NW Bethany Southbound'],
            ['10107', 'NW Bethany &amp; Laidlaw Southbound'],
            ['10114', 'NW Bethany &amp; Oak Hills Dr Southbound'],
            ['8920',  'SW Walker &amp; Butner Westbound'],
            ['5590',  'SW Tualatin Valley Hwy &amp; Market Centre Eastbound'],
            ['10111', 'NW Bethany &amp; West Union Southbound'],
            ['10089', 'NW Bethany &amp; West Union Northbound'],
            ['13685', 'NW Laidlaw &amp; Bethany Eastbound'],
            ['6830',  'SW 158th &amp; Jay Northbound'],
    ]

    route_stops = [
            ['929',  ['044....">44</a>', '054....">54</a>', '056....">56</a>'] ],
    ]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_stops_near_geocode_route_stops(self):
        for m in ['', 'm/']:
            for s in self.route_stops:
                url = get_url(m + 'stops_near.html', 'place=' + s[0])
                self.call_url_match_list(url, s[1])

    def test_stops_near_geocode(self):
        for m in ['', 'm/']:
            for s in self.stops:
                url = get_url(m + 'stops_near.html', 'place=' + s[0])
                self.call_url_match_string(url, s[1])

    def test_geocode(self):
        for m in ['', 'm/']:
            url = get_url(m + 'planner.html', 'from=834 SE')
            self.call_url_match_list(url, ["834 SE MILL", "834 SE LAMBERT"])


#class DontRunTests():
class ViewTests(MyTestCase):

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

    def test_stops_near(self):
        for m in ['', 'm/']:
            url = get_url(m + 'stops_near.html', 'placeCoord=45.5,-122.5&place=XTCvsAdamAnt')
            s = call_url(url)
            self.assertRegexpMatches(s,"SE Division")
            self.assertRegexpMatches(s,"XTCvsAdamAnt")

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

    def test_homepage_form(self):
        url = get_url('pform_standalone.html', 'from=PDX::45.587546,-122.592925&to=ZOO')
        s = call_url(url)
        self.assertRegexpMatches(s, 'type="text" id="from" name="from" value="PDX"')
        self.assertRegexpMatches(s, 'type="text" id="going" name="to" value="ZOO"')

