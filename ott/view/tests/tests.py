import unittest
from pyramid import testing

import urllib
import contextlib
import json

PORT="33333"

class TestMyView(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

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

    def test_plan_form(self):
        for m in ['', 'm/']:
            url = get_url(m + 'planner_form.html', 'from=PDX&to=ZOO::45.495883,-122.501919')
            s = call_url(url)
            self.assertRegexpMatches(s, 'type="text"   id="from" name="from" value="PDX"')
            self.assertRegexpMatches(s, 'type="text"   id="going" name="to" value="ZOO"')


    def test_plan_trip(self):
        for m in ['', 'm/']:
            url = get_url(m + 'planner.html', 'to=pdx&from=zoo&Hour=9&Minute=0&AmPm=pm')
            s = call_url(url)
            self.assertRegexpMatches(s,"MAX Red Line")

    def test_plan_walk(self):
        for m in ['', 'm/']:
            url = get_url(m + 'planner_walk.html', 'mode=WALK&from=pdx&to=zoo')
            s = call_url(url)
            self.assertRegexpMatches(s,"Airport Way")

    def test_map_place(self):
        for m in ['', 'm/']:
            url = get_url(m + 'map_place.html', 'name=834 SE MILL ST&city=Portland&lon=-122.65705&lat=45.509865')
            s = call_url(url)
            self.assertRegexpMatches(s,"Plan a trip to 834 SE MILL ST")
            self.assertRegexpMatches(s,"ride.trimet.org")

    def test_geocode(self):
        for m in ['', 'm/']:
            url = get_url(m + 'planner.html', 'from=834 SE')
            s = call_url(url)
            self.assertRegexpMatches(s, "834 SE MILL")
            self.assertRegexpMatches(s, "834 SE LAMBERT")

    def test_homepage_form(self):
        url = get_url('pform_standalone.html', 'from=PDX&to=ZOO')
        s = call_url(url)
        self.assertRegexpMatches(s, 'type="text"   id="from" name="from" value="PDX"')
        self.assertRegexpMatches(s, 'type="text"   id="going" name="to" value="ZOO"')


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

