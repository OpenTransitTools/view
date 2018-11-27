from ott.utils.tests.ott_test_case import OttTestCase


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
        """ check that the following place queries hit a stop page (via the stop image url)
        """
        places = [
            "2",
            "A+Ave+Chandler+Lake+Oswego+(Stop+ID+2)",
            "Stop ID 8",
        ]
        for l in [None, 'es']:
            for m in ['', 'm/']:
                for p in places:
                    url = self.get_url(m + 'stops_near.html', 'place=' + p, l)
                    self.call_url_match_string(url, "stop[_schedule]*.html.stop_id.")

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
