<%namespace name="util"  file="/shared/utils/misc_utils.mako"/>
<%
    extra_params = util.get_extra_params()
    rel_path='./'
    if util.has_url_param('mobile'):
        rel_path = './m/'
    pages = [
        {'label': 'Trip Planner Pages'},
        {'u':'planner_form.html', 'p':'from=2'},
        {'u':'planner.html', 'p':'from=834&toCoord=45.363514%2C-122.59389&to=900+Block+Abernethy%2C+Oregon+City&time=11:11',   'n':"uncertain 'from' location"},
        {'u':'planner.html', 'p':'to=834&fromCoord=45.363514%2C-122.59389&from=900+Block+Abernethy%2C+Oregon+City&time=11:11', 'n':"uncertain 'to' location"},
        {'u':'planner_geocode.html', 'p':'', 'n':"no geocoder options list (and neither from / to)"},
        {'u':'planner.html', 'p':'from=2::-122.5,45.5&to=zoo::-122.5,45.5&Hour=12&Minute=35&AmPm=pm'},
        {'u':'planner.html', 'p':'from=2::-122.5,45.5&to=zoo::-122.5,45.5&Hour=12&Minute=35&AmPm=pm&mode=BICYCLE', 'n':'Bike Only Trip'},
        {'u':'planner_walk.html', 'p':'mode=WALK&from=45.448814,-122.631935&to=45.443102,-122.636399', 'n':'NOTE: Separate Walk Direction Planner Page'},
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
    <h2>Welcome to the Trip Tools testing area!</h2>
    <p>Use the links below to test out the Trip Planner and its related pages.</p>
    <p>We'll probably want to cull this list a bit for the official testing. Reorganize, too. But we need to keep this page as-is... maybe make it test.html or something like that.</p>

    %for p in pages:
        %if 'label' in p:
            <h2>${p['label']}</h2>
        %else:
            <a target="_blank" href="${p['path'] if 'path' in p else rel_path}${p['u']}?${p['p']}${extra_params}">${p['u']}</a>  ${p['n'] if 'n' in p else ''}<br/>
        %endif
    %endfor
