## -*- coding: utf-8 -*-
## 
## library of routines that enable jQuery autocomplete routine for abitrary input form(s)
## (geocoder mostly)
##
<%namespace name="util"  file="/shared/utils/misc_util.mako"/>

#
# search list form
# Scrolling List of Possible Locations
#
<%def name="jquery_includes()">
    <link href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet" />
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
</%def>

<%def name="custom_css()">
    <style>
    .ui-autocomplete-loading { background: white url('busy.gif') right center no-repeat; }
    .ui-autocomplete {
        max-height: 210px;
        overflow-y: auto;
        overflow-x: hidden; /* prevent horizontal scrollbar */
    }
    /* IE 6 doesn't support max-height we use height instead, but this forces the menu to always be this tall */
    * html .ui-autocomplete {
        height: 100px;
    }
    </style>
</%def>

<%def name="custom_js(def_url='http://maps5.trimet.org/solr/select', num_rows='20')">
    <script>
    function SOLRAutoComplete(input_div, log_div, solr_url)
    {
        this.input_div = input_div || "#input";
        this.log_div   = log_div   || "#log";
        this.solr_url  = solr_url  || "${def_url}";

        function log(log_div, message)
        {
            $("<div/>").text( message ).prependTo(log_div);
            $(log_div).attr( "scrollTop", 0 );
        }

        function solr_callback(term, response)
        {
            console.log(term);
            response();
        }

        function enable_ajax()
        {
            var THIS = this;

            $(THIS.input_div).autocomplete({
                minLength: 1,
                delay: 500,
                source: function( request, response ) {
                    $.ajax({
                        type:     "GET",
                        dataType: "json",
                        url:      THIS.solr_url,
                        data: {
                            q:  request.term,
                            wt: "json",
                            qt: "dismax",
                            rows: "20"
                        },
                        cache: false,
                        success: function(resp, resp_code) {
                            docs = resp.response.docs;
                            len=docs.length;
                            var data=[];
                            for(var i=0; i < len; i++)
                            {
                                var lab = docs[i].name;
                                if(docs[i].city && docs[i].city.length > 0 && docs[i].city != 'undefined')
                                    lab = lab + " (" + docs[i].city + ")";
                                var s = {"id": docs[i].id, "label": lab, "value": lab, "solr_doc":docs[i]};
                                data.push(s);
                            }

                            response(data);
                        }
                    });
                },
                minLength: 0,
                select: function(event, ui) {
                        console.log(ui.item.solr_doc);
                        log(THIS.log_div, ui.item ?
                            "${_(u'Selected')}: " + ui.item.value + ", geonameId: " + ui.item.id :
                            "${_(u'Nothing selected, input was')}: " + this.value );
                } 
            });
        }
        this.enable_ajax=enable_ajax;
    };
</%def>

<%def name="find_stop()">
    <script>
    // main entry 
    $(function(){
        stop = new SOLRAutoComplete('#stop');
        stop.enable_ajax();
    });
    </script>
</%def>

<%def name="trip_planner()">
    <script>
    // main entry 
    $(function(){
        fm = new SOLRAutoComplete('#from');
        fm.enable_ajax();
        to = new SOLRAutoComplete('#to', '#xlog');
        to.enable_ajax();
    });
    </script>
</%def>