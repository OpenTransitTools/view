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
        # desktop
        url = get_url('stop_select_form.html')
        s = call_url(url)
        self.assertRegexpMatches(s,"MAX Blue")

        # mobile
        url = get_url('m/stop_select_form.html')
        s = call_url(url)
        self.assertRegexpMatches(s,"MAX Blue")

    def test_stop_select_list(self):
        ''' route stops ws: stop select for each route direction '''
        url = get_url('stop_select_list.html', 'route=100')
        s = call_url(url)
        self.assertRegexpMatches(s,"MAX Blue")
        self.assertRegexpMatches(s,"Hatfield")

        url = get_url('m/stop_select_list.html', 'route=100')
        s = call_url(url)
        self.assertRegexpMatches(s,"MAX Blue")
        self.assertRegexpMatches(s,"Hatfield")

    def test_stop(self):
        url = get_url('stop.html', 'stop_id=2')
        s = call_url(url)
        self.assertRegexpMatches(s,"Lake Oswego")

    def test_stops_near(self):
        url = get_url('stops_near.html', 'placeCoord=45.5,-122.5&place=XTCvsAdamAnt')
        s = call_url(url)
        self.assertRegexpMatches(s,"SE Division")
        self.assertRegexpMatches(s,"XTCvsAdamAnt")

'''
    def test_stop_schedule(self):
        url = get_url('stop_schedule.html', 'stop_id=2')
        self.assertRegexpMatches(s,"Lake Oswego")

    def test_plan_trip(self):
        url = get_url('plan_trip.html', 'from=pdx&to=zoo')
        j = call_url(url)
        s = json.dumps(j)
        #self.assertEqual(j['status_code'], 200)
        self.assertRegexpMatches(s,"Zoo")
        self.assertRegexpMatches(s,"itineraries")

    def test_geocode(self):
        url = get_url('geocode', 'place=zoo')
        self.assertRegexpMatches(s,"-122.71")
        self.assertRegexpMatches(s,"45.51")
'''

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

