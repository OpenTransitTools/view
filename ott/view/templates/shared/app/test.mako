<%namespace name="util"  file="/shared/utils/misc_util.mako"/>
<%
    extra_params = util.get_extra_params()
    rel_path='./'
    if util.has_url_param('mobile'):
        rel_path = './m/'
    pages = [
        {'label': 'Trip Planner Pages'},
        {'u':'planner_form.html', 'p':'from=2'},
        {'u':'planner_geocode.html', 'p':'place=d&type=from', 'n':"uncertain 'from' location"},
        {'u':'planner_geocode.html', 'p':'place=d&type=to',   'n':"uncertain 'to' location"},
        {'u':'planner_geocode.html', 'p':'', 'n':"no geocoder options list (and neither from / to)"},
        {'u':'planner.html', 'p':'from=2&to=zoo&Hour=12&Minute=35&AmPm=pm'},
        {'u':'planner.html', 'p':'from=2&to=zoo&Hour=12&Minute=35&AmPm=pm&mode=BICYCLE', 'n':'Bike Only Trip'},
        {'u':'planner_walk.html', 'p':'mode=WALK&from=45.448814,-122.631935&to=45.443102,-122.636399', 'n':'NOTE: Separate Walk Direction Planner Page'},
        {'u':'adverts.html', 'p':'', 'n':'Adverts testing page'},
        {'u':'http://dev.trimet.org/map/trimet-ssi.htm', 'path':'', 'p':'from=zoo&to=pdx', 'n':'example of the embedded form page via server-side includes (note the url params populating the form, and the Spanish localization)'},
        {'u':'', 'p':'', 'n':''},

        {'label': 'Stop Pages'},
        {'u':'stop_select_form.html', 'p':'test'},
        {'u':'stop_select_list.html', 'p':'route=100'},
        {'u':'stop_select_geocode.html', 'p':'place=8+NW+8TH+AVE%2C+PORTLAND'},
        {'u':'stop_select_geocode.html', 'p':'', 'n':'no geocoder option select list'},
        {'u':'stop.html', 'p':'stop_id=2'},
        {'u':'stops_near.html', 'p':'place=2', 'n':'(hit a geocode directly ... go directly to stop page)'},
        {'u':'stops_near.html', 'p':'place=SE+D+ST+%26+SE+D+PL%2C+Milwaukie', 'n':'(ambiguous ... calls geocoder)'},
        {'u':'stops_near.html', 'p':'place=SE+D+ST+%26+SE+D+PL%2C+Milwaukie&placeCoord=45.52321,-122.678246', 'n':'(has placeCoord, which will do stops near)'},
        {'u':'stops_near.html', 'p':'place=SE+D+ST+%26+SE+D+PL::45.4488,-122.63193::Milwaukie', 'n':'(has placeGeocode do direct to stops near)'},
        {'u':'stops_near.html', 'p':'has_geocode=true&place=SE+D+ST+%2526+SE+D+PL::45.448814,-122.63193::Milwaukie', 'n':'(use place::geo_code, which will do stops near)'},
        {'u':'stops_near.html', 'p':'place=834 SE Mill St&show_more=true', 'n':'(show more link -- full 20 stops nearby address...)'},
        {'u':'map_place.html',  'p':'name=834 SE MILL ST&city=Portland&lon=-122.65705&lat=45.509865'},

        {'label': 'Stop Schedule'},
        {'u':'stop_schedule.html', 'p':'stop_id=11507&route=190', 'n':'Single Route Listing'},
        {'u':'stop_schedule.html', 'p':'stop_id=11507', 'n':'All routes for stop'},
        {'u':'stop_schedule.html', 'p':'stop_id=11507&sort=time', 'n':'sort by time'},
        {'u':'stop_schedule.html', 'p':'stop_id=11507&more', 'n':'more button'},
    ] 
%>
    <button onclick="location.href='.'">ENGLISH</button> <button onclick="location.href='.?_LOCALE_=es'">SPANISH</button> <button onclick="location.href='.?mobile=1${extra_params}'">MOBILE</button>
    <br/>
    <h1>
    %if 'm' in rel_path:
        MOBILE |
    %else:
        DESKTOP |
    %endif
    %if len(extra_params) > 1:
        SPANISH
    %else:
        ENGLISH
    %endif
    </h1>
    %for p in pages:
        %if 'label' in p:
            <h2>${p['label']}</h2>
        %else:
            <a target="#" href="${p['path'] if 'path' in p else rel_path}${p['u']}?${p['p']}${extra_params}">${p['u']}</a>  ${p['n'] if 'n' in p else ''}<br/>
        %endif
    %endfor
