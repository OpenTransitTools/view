if(window.console == undefined) window.console = {};
if(window.console.log == undefined) window.console = function(el){};

function DynamicPlannerForms(walk_label, bike_label, short_dist, long_dist)
{
    this.walk_label = walk_label || 'Walk distance';
    this.bike_label = bike_label || 'Bike distance';

    this.short_dist = short_dist || 1260;
    this.long_dist  = long_dist  || 4828;

    function do_walk_only()
    {
        $("#trip-transfers option[value=TRANSFERS]").hide();
        $("#trip-transfers option[value=SAFE]").hide();
        $('#trip-transfers').val('QUICK').change();
        $('#trip-walkdistance').val(this.long_dist).change();
        $('label[for=trip-walkdistance]').html(this.walk_label);
    }
    this.do_walk_only = do_walk_only;

    function do_bike_only()
    {
        $("#trip-transfers option[value=TRANSFERS]").hide();
        $("#trip-transfers option[value=SAFE]").show();
        $('#trip-transfers').val('SAFE').change();
        $('#trip-walkdistance').val(this.short_dist).change();
        $('label[for=trip-walkdistance]').html(this.bike_label);
    } 
    this.do_bike_only = do_bike_only;

    function do_bike_transit()
    {
        $("#trip-transfers option[value=TRANSFERS]").show();
        $("#trip-transfers option[value=SAFE]").show();
        $('#trip-transfers').val('SAFE').change();
        $('#trip-walkdistance').val(this.long_dist).change();
        $('label[for=trip-walkdistance]').html(this.bike_label);
    }
    this.do_bike_transit = do_bike_transit;

    function do_transit()
    {
        $("#trip-transfers option[value=TRANSFERS]").show();
        $("#trip-transfers option[value=SAFE]").hide();
        $('#trip-transfers').val('QUICK').change();
        $('#trip-walkdistance').val(this.short_dist).change();
        $('label[for=trip-walkdistance]').html(this.walk_label);
    }
    this.do_transit = do_transit;


    function switch_modes(mode)
    {
        if(mode == "WALK")
            this.do_walk_only();
        else if(mode == "BICYCLE")
            this.do_bike_only();
        else if(mode.indexOf("BICYCLE") >= 0)
            this.do_bike_transit();
        else
            this.do_transit();
    }
    this.switch_modes = switch_modes;
}
