

class AgencyTemplate(object):
    def __init__(self):
        ''' 
             TODO: read a config file, to populate this cache for different agencies
        '''
        self.template_cache = { 
                'TriMet' : {
                    'desktop' : {
                        'arrivals'   : 'http://trimet.org/arrivals/tracker?stopID={stop_id}',
                        'alerts'     : 'http://trimet.org/alerts',
                        'stop_img'   : 'http://ride.trimet.org/eapi/ws/V1/stopimage/format/png/width/{w}/height/{h}/zoom/{z}/excparams/format_options=layout:scale/id/{stop_id}',
                        'imap'       : 'http://ride.trimet.org/?zoom=16&pLat={lat}&pLon={lon}&pText={name}',
                        'route'      : 'http://trimet.org/schedules/r{route_id:03d}.htm',
                    },
                    'mobile' : {
                        'arrivals'   : 'http://trimet.org/arrivals/small/tracker?stopID={stop_id}',
                        'alerts'     : 'http://trimet.org/m/alerts',
                        'stop_img'   : 'http://ride.trimet.org/eapi/ws/V1/stopimage/format/png/width/{w}/height/{h}/zoom/{z}/excparams/format_options=layout:scale/id/{stop_id}',
                        'route'      : 'http://trimet.org/images/schedulemaps/{route_id:03d}.gif',
                    },
                }
        }


    def get_template(self, template, agency='TriMet', device='desktop', def_val=None):
        ret_val = def_val
        try:
            ret_val = self.template_cache[agency][device][template]
        except:
            pass
        return ret_val


    def get_arrivals_url(self, stop_id, route_id=None, route_fmt="route={route_id}", agency='TriMet', device='desktop', def_val=None):
        ret_val = def_val
        url = self.get_template('arrivals', agency, device, def_val)
        if url != def_val:
            p = {'stop_id':stop_id}
            if route_id and route_fmt:
                p['route_id'] = route_id
                url += "&" + route_fmt
            ret_val = url.format(**p)
        return ret_val

    def get_alerts_url(self, route_id=None, route_fmt="route={route_id}", agency='TriMet', device='desktop', def_val=None):
        ret_val = def_val
        url = self.get_template('alerts', agency, device, def_val)
        if url != def_val:
            ret_val = url
            if route_id and route_fmt:
                p = {}
                p['route_id'] = route_id
                url += "?" + route_fmt
                ret_val = url.format(**p)
        return ret_val

    def get_stop_img_url(self, stop_id, w=275, h=275, z=6, agency='TriMet', device='desktop', def_val=None):
        ret_val = def_val
        url = self.get_template('stop_img', agency, device, def_val)
        if url != def_val:
            p = {'stop_id':stop_id, 'w':w, 'h':h, 'z':z}
            ret_val = url.format(**p)
        return ret_val

    def get_interactive_map_url(self, lat, lon, name="", route_id=None, agency='TriMet', device='desktop', def_val=None):
        ret_val = def_val
        url = self.get_template('imap', agency, device, def_val)
        if url != def_val:
            p = {'name':name, 'lat':lat, 'lon':lon}
            ret_val = url.format(**p)
        return ret_val

    def get_route_url(self, route_id, agency='TriMet', device='desktop', def_val=None):
        ret_val = def_val
        url = self.get_template('route', agency, device, def_val)
        if url != def_val:
            p = {'route_id':route_id}
            ret_val = url.format(**p)
        return ret_val

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