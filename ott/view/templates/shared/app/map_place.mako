<%namespace name="util"  file="/shared/utils/misc_utils.mako"/>
<%namespace name="su"    file="/shared/utils/stop_utils.mako"/>
<%
    extra_params = util.get_extra_params()
%>

${su.simple_header(sub_title=util.name_city_str_from_struct(place))}

<div class="fullwidth">
    <div class="contentcontainer">
        <div class="row">
            <div class="col-xs-12 col-md-8 col-lg-8">
                %if place['lat'] and place['lon']:
                ${su.place_map(place['name'], place['lon'], place['lat'], extra_params)}
                %endif
            </div><!-- .col -->
            <div class="col-xs-12 col-md-4 col-lg-4">
                %if place['lat'] and place['lon']:
                ${util.plan_a_trip_links(place['name'], place['lon'], place['lat'], extra_params)}
                %endif
            </div><!-- .col -->
      </div><!-- .row -->
    </div><!-- .contentcontainer -->
</div><!-- .fullwidth -->
