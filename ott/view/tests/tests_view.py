from ott.utils.tests.ott_test_case import OttTestCase


class ViewTests(OttTestCase):

    def test_stops_near(self):
        for m in ['', 'm/']:
            # test place and placeCoord
            url = self.get_url(m + 'stops_near.html', 'placeCoord=45.5,-122.5&place=XTCvsAdamAnt')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "miles away")
            self.assertRegexpMatches(s, "SE Division")
            self.assertRegexpMatches(s, "XTCvsAdamAnt")

            # test named coord
            url = self.get_url(m + 'stops_near.html', 'place=834 SE LAMBERT ST::45.468602,-122.657627')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "miles away")

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
            self.assertRegexpMatches(s, "MAX Blue")

    def test_stop_select_list(self):
        ''' route stops ws: stop select for each route direction '''
        for m in ['', 'm/']:
            url = self.get_url(m + 'stop_select_list.html', 'route=100')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "MAX Blue")
            self.assertRegexpMatches(s, "Hatfield")

    def test_stop(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'stop.html', 'stop_id=2')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "Lake Oswego")

    def test_localization(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'stop.html', 'stop_id=2&_LOCALE_=es')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "Lake Oswego")

    def test_stop_schedule(self):
        for m in ['', 'm/']:
            for t in ['&sort=destination', '&sort=time']:
                url = self.get_url(m + 'stop_schedule.html', 'stop_id=2' + t)
                s = self.call_url(url)
                self.assertRegexpMatches(s, "Lake Oswego")

                url = self.get_url(m + 'stop_schedule.html', 'stop_id=2&more' + t)
                s = self.call_url(url)
                self.assertRegexpMatches(s, "Lake Oswego")

    def test_plan_form(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'planner_form.html', 'from=PDX::45.587546,-122.592925&to=ZOO')
            s = self.call_url(url)
            self.assertRegexpMatches(s, 'type="text" id="from" name="from" value="PDX"')
            self.assertRegexpMatches(s, 'type="text" id="going" name="to" value="ZOO"')

    def test_plan_trip(self):
        url = self.ini.get('ott.host_url', 'app:main')
        mailto = "mailto.*{}.*planner.html".format(url.replace(":", "%3A"))
        for m in ['', 'm/']:
            url = self.get_url(m + 'planner.html', 'to=pdx::45.587546,-122.592925&from=zoo::45.5092,-122.7133&Hour=9&Minute=0&AmPm=pm')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "MAX Red Line")
            self.assertRegexpMatches(s, mailto)

    def test_plan_walk(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'planner_walk.html', 'mode=WALK&from=pdx::45.587546,-122.592925&to=zoo')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "Airport Way")

    def test_map_place(self):
        for m in ['', 'm/']:
            url = self.get_url(m + 'map_place.html', 'name=834 SE MILL ST&city=Portland&lon=-122.65705&lat=45.509865')
            s = self.call_url(url)
            self.assertRegexpMatches(s, "Plan a trip to 834 SE MILL ST")
