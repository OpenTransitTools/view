''' Agency Template is a set of urls specific to the agencies home website for other 
    infomration webapps that the trip planner can link to (like alerts services, real-time 
    vehicle predictions, maps, etc...)
'''
import re


AGENCY_TEMPLATE = None

def make_url_template():
    ''' 
    '''
    global AGENCY_TEMPLATE
    if AGENCY_TEMPLATE is None:
        AGENCY_TEMPLATE = AgencyTemplate()
    return AGENCY_TEMPLATE


class AgencyTemplate(object):
    def __init__(self):
        ''' TODO: read a config file, to populate this cache for different agencies
        '''
        self.template_cache = { 
                'TriMet' : {
                    'desktop' : {
                        'arrivals'   : 'http://trimet.org/#tracker/stop/{stop_id}/',
                        'alerts'     : 'http://trimet.org/#alerts/',
                        'stop_img'   : 'http://ride.trimet.org/eapi/ws/V1/stopimage/format/png/width/{w}/height/{h}/zoom/{z}/excparams/format_options=layout:scale/id/{stop_id}',
                        'imap'       : 'http://ride.trimet.org/?zoom=16&pLat={lat}&pLon={lon}&pText={name}',
                        'route'      : 'http://trimet.org/schedules/r{route_id:0>3}.htm',
                    },
                    'mobile' : {
                        'arrivals'   : 'http://trimet.org/arrivals/small/tracker?stopID={stop_id}',
                        'alerts'     : 'http://trimet.org/m/alerts',
                        'stop_img'   : 'http://ride.trimet.org/eapi/ws/V1/stopimage/format/png/width/{w}/height/{h}/zoom/{z}/excparams/format_options=layout:scale/id/{stop_id}',
                        'route'      : 'http://trimet.org/schedules/img/{route_id:0>3}.png',
                    },
                }
        }

        ''' TODO: make agency=None in param calls, and use the get_agency() call to initialize '''
        self.default_agency = 'TriMet'
        self.route_id_cleanup = '\D.*'

    def clean_route_id(self, route_id):
        ''' cleans the route_id parameter.  needed because TriMet started using id.future type route ids for route name changes
        '''
        ret_val = route_id
        if self.route_id_cleanup:
            ret_val = re.sub(self.route_id_cleanup, '', route_id)
        return ret_val

    def get_agency(self, agency):
        if agency is None:
            agency = self.default_agency
        return agency

    def get_template(self, template, agency=None, device='desktop', def_val=None):
        ret_val = def_val
        agency = self.get_agency(agency)
        try:
            if isinstance(device, bool):
                device = self.device_type(device)
            ret_val = self.template_cache[agency][device][template]
        except Exception, e:
            #log.debug(e)
            pass
        return ret_val

    def device_type(self, is_mobile=False):
        return 'mobile' if is_mobile else 'desktop'

    def get_arrivals_url(self, stop_id, route_id=None, route_fmt="route={route_id}", agency=None, device='desktop', def_val=None):
        ret_val = def_val
        agency = self.get_agency(agency)
        url = self.get_template('arrivals', agency, device, def_val)
        if url != def_val:
            p = {'stop_id':stop_id}
            if route_id and route_fmt:
                p['route_id'] = self.clean_route_id(route_id)
                url += "&" + route_fmt
            ret_val = url.format(**p)
        return ret_val

    def get_alerts_url(self, route_id=None, route_fmt="route={route_id}", agency=None, device='desktop', def_val=None):
        ret_val = def_val
        agency = self.get_agency(agency)
        url = self.get_template('alerts', agency, device, def_val)
        if url != def_val:
            ret_val = url
            if route_id and route_fmt:
                p = {}
                p['route_id'] = self.clean_route_id(route_id)
                url += "?" + route_fmt
                ret_val = url.format(**p)
        return ret_val

    def get_stop_img_url(self, stop_id, w=275, h=275, z=7, agency=None, device='desktop', def_val=None):
        ret_val = def_val
        agency = self.get_agency(agency)
        url = self.get_template('stop_img', agency, device, def_val)
        if url != def_val:
            p = {'stop_id':stop_id, 'w':w, 'h':h, 'z':z}
            ret_val = url.format(**p)
        return ret_val

    def get_interactive_map_url(self, lat, lon, name="", route_id=None, agency=None, device='desktop', def_val=None):
        ret_val = def_val
        agency = self.get_agency(agency)
        url = self.get_template('imap', agency, device, def_val)
        if url != def_val:
            p = {'name':name, 'lat':lat, 'lon':lon}
            ret_val = url.format(**p)
        return ret_val

    def get_route_url(self, route_id, agency=None, device='desktop', def_val=None):
        #import pdb; pdb.set_trace()
        ret_val = def_val
        agency = self.get_agency(agency)
        url = self.get_template('route', agency, device, def_val)
        if url != def_val:
            p = {'route_id':self.clean_route_id(route_id)}
            ret_val = url.format(**p)
        return ret_val

    def mobile_route_url(self, route_id, agency=None, def_val=None):
        return self.get_route_url(route_id, agency, 'mobile', def_val)
    def desktop_route_url(self, route_id, agency=None, def_val=None):
        return self.get_route_url(route_id, agency, 'desktop', def_val)

def test():
    a = AgencyTemplate()
    for d in ['desktop', 'mobile']:
        print a.get_arrivals_url(2, device=d)
        print a.get_arrivals_url(2, 78, device=d)
        print a.get_alerts_url(device=d)
        print a.get_alerts_url(1, device=d)
        print a.get_stop_img_url(2, device=d)
        print a.get_interactive_map_url(3, 4, device=d)
        print a.get_route_url(1, device=d)

if __name__ == "__main__":
    test()
