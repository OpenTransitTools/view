from ott.view.utils import html_utils
from ott.view.locale.subscribers import get_translator

class Place(object):
    def __init__(self, name=None, lat=None, lon=None, city=None):
        self.set_values(name, lat, lon, city)

    def set_values(self, name=None, lat=None, lon=None, city=None):
        self.name = name
        self.lat = lat 
        self.lon = lon
        self.city = city

    def set_values_via_place_str(self, place):
        ''' will set the values of a <name>::<lat>,<lon>::<city> string into a place object
            ala PDX::45.5,-122.5::Portland will populate the Place object attributes
        '''
        try:
            # import pdb; pdb.set_trace() 
            p = place.split("::")
            if p[0] and len(p[0]) > 0:
                self.name = p[0]
            if p[1] and len(p[1]) > 0 and ',' in p[1]:
                ll = p[1].split(',')
                if ll and len(ll) >= 2:
                    self.lat = ll[0].strip()
                    self.lon = ll[1].strip()
            if p[2] and len(p[2]) > 0:
                self.city = p[2]
        except:
            pass


    @classmethod
    def make_from_request(cls, request):
        ret_val = Place()
        try:
            name = html_utils.get_first_param(request, 'name')
            if name is None:
                _  = get_translator(request) 
                name = _(u'Uncertain location')

            lat  = html_utils.get_first_param(request, 'lat')
            lon  = html_utils.get_first_param(request, 'lon')
            city = html_utils.get_first_param(request, 'city')
            ret_val.set_values(name, lat, lon, city)

            place = html_utils.get_first_param(request, 'place')
            ret_val.set_values_via_place_str(place)
        except: pass
        return ret_val

