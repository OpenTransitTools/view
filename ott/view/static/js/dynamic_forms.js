if(window.console == undefined) window.console = {};
if(window.console.log == undefined) window.console = function(el){};

function DynamicForms(walk_label, bike_label, short_dist, long_dist)
{
    this.walk_label = walk_label || 'Walk distance';
    this.bike_label = bike_label || 'Bike distance';

    this.short_dist = short_dist || 1609;
    this.long_dist  = long_dist  || 4828;

    function do_walk_only(change)
    {
        $("#trip-transfers option[value='TRANSFERS']").hide();
        $("#trip-transfers option[value='SAFE']").hide();
        $("#trip-transfers option[value='SAFE']").css('display','none');
        $('label[for=trip-walkdistance]').html(this.walk_label);
        if(change) {
            $('#trip-transfers').val('QUICK').change();
            $('#trip-walkdistance').val(this.long_dist).change();
        }
    }
    this.do_walk_only = do_walk_only;

    function do_bike_only(change)
    {
        $("#trip-transfers option[value='TRANSFERS']").hide();
        $("#trip-transfers option[value='SAFE']").show();
        $('label[for=trip-walkdistance]').html(this.bike_label);
        if(change) {
            $('#trip-transfers').val('SAFE').change();
            $('#trip-walkdistance').val(this.long_dist).change();
        }
    } 
    this.do_bike_only = do_bike_only;

    function do_bike_transit(change)
    {
        $("#trip-transfers option[value='TRANSFERS']").show();
        $("#trip-transfers option[value='SAFE']").show();
        $('label[for=trip-walkdistance]').html(this.bike_label);
        if(change) {
            $('#trip-transfers').val('SAFE').change();
            $('#trip-walkdistance').val(this.long_dist).change();
        }
    }
    this.do_bike_transit = do_bike_transit;

    function do_transit(change)
    {
        $("#trip-transfers option[value='TRANSFERS']").show();
        $("#trip-transfers option[value='SAFE']").hide();
        $('label[for=trip-walkdistance]').html(this.walk_label);
        if(change) {
            $('#trip-transfers').val('QUICK').change();
            $('#trip-walkdistance').val(this.short_dist).change();
        }
    }
    this.do_transit = do_transit;


    function switch_mode(mode, change)
    {
        if(mode == null)
            mode = $('#trip-modetype option:selected').val();

        if(mode == "WALK")
            this.do_walk_only(change);
        else if(mode == "BICYCLE")
            this.do_bike_only(change);
        else if(mode.indexOf("BICYCLE") >= 0)
            this.do_bike_transit(change);
        else
            this.do_transit(change);
    }
    this.switch_mode = switch_mode;

    /** 
     * call me to setup the mode switcher method above...
     */
    function add_mode_callback(tgt)
    {
        var target = tgt || '#trip-modetype';
        var THIS   = this;
        $(target).change(function() {
            THIS.switch_mode(null, true);
        });
    }
    this.add_mode_callback = add_mode_callback;
}
