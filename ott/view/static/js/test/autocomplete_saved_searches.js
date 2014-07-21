if(window.console == undefined) window.console = {};
if(window.console.log == undefined) window.console = function(el){};


/**
 * SOLRAutoComplete class that will call SOLR, and return text data...
 * new SOLRAutoComplete('#input_div_id')
 * 
 * @param {Object} input_div
 * @param {Object} solr_url
 * @param {Object} num_results
 */
function SOLRAutoComplete(input_div, solr_url, num_results)
{
    this.input_div   = input_div   || "#input";
    this.solr_url    = solr_url    || "http://127.0.0.1/solr/select";
    this.num_results = num_results || "6";


    /** callback (that you override) to get the resulting clicked SOLR document */
    function select_callback(sel)
    {
        console.log('Selected:' + sel.value + ", id: " + sel.id + " " + this.solr_url);
    }
    this.select_callback = select_callback;

    /** 
     * function that controls the naming of the geo point
     * NOTE: this isn't localized (e.g., type name and city conjunction), so override in .mako
     *
     * @return: formatted place name, ala 844 SE X Street, Portland -or- A Ave, Portalnd (Stop ID 2)  
     */
    function place_name_format(name, city, type, id)
    {
        var ret_val = name;
        try {
            var stop = ''
            if(type == 'stop')
                stop = " (Stop ID " + id + ")";
            ret_val = name + city + stop;
        }
        catch(e) {
        }
        return ret_val;
    }
    this.place_name_format = place_name_format;

    function get_saved_searches(term) {
        var ret_val = [];
        var searchT_raw = localStorage.getItem('searchTerms');
        if (searchT_raw !== null) {
            var searchT = JSON.parse(searchT_raw);
         
            //check that saved search terms match current search term
            for (var key in searchT) {
                if (searchT.hasOwnProperty(key) && 
                        key.toUpperCase().substring(0, term.length) === term.toUpperCase()) {
                    ret_val.push(searchT[key]);
                }
            }
        }
        return ret_val;
    }

    function enable_ajax()
    {
        var THIS = this;  // make SOLRAutoComplete instance 'this' available to jQuery ajax stuff below 

        $(THIS.input_div).autocomplete(
        {
            minLength : 1,
            delay     : 500,
            source : function(request, response) {
                $.ajax({
                    type : "GET",
                    dataType : "json",
                    url : THIS.solr_url,
                    data : {
                        rows : THIS.num_results,
                        wt : "json",
                        qt : "dismax",
                        fq : "(-type:26 AND -type:route)",
                        q : request.term
                    },
                    cache : false,

                    success : function(resp, resp_code)  // jQuery ajax callback
                    {
                        
                        //var searchT = get_saved_searches();
                      
                        // step 0: SOLR elements...
                        docs = resp.response.docs;
                        len = docs.length;

                        // step 1: loop through SOLR results, and build data object required for jQ's autocomplete 
                        var data = get_saved_searches(request.term);

                        for (var i = 0; i < len; i++)
                        {
                            var doc = docs[i];

                            // step 2: make a label out of name, type_name and optionally city and stop id
                            var city = '';
                            if (doc.city && doc.city.length > 0)
                                city = ", " + doc.city;

                            var id = doc.id;
                            if (doc.type == 'stop')
                                id = doc.stop_id;

                            var label = THIS.place_name_format(doc.name, city, doc.type, id);
                             
                            // step 3: make the autocomplete object, and add it to our return array
                            var s = {
                                "id"       : doc.id,
                                "label"    : label,
                                "value"    : label,
                                "solr_doc" : doc,
                                "saved"    : false
                            };
                            data.push(s);
                        }
                        // step 4: jQuery UI autocomplete (required) callback
                        response(data);
                    }
                });
            },

            /** jQuery autocomplete selected value callback */
            select : function(event, ui)
            {
                try {
                    // call our custom callback with the SOLR document
                    THIS.select_callback(ui.item);
                } catch(e) {
                    try { console.log("SOLRAutoComplete - select callback: " + e); }
                    catch(e) {}
                }
            }
        
        // set custom display for autocomplete results
        // render saved search terms different than solr results
        
        // TODO: add 'remove' link for saved search terms

        }).data("ui-autocomplete")._renderItem = function(ul, item) {
            

            if(item.saved === true) {
                return $("<li></li>")
                    .data("item.autocomplete", item)
                    .append("<a><b>" + item.label + "</b></a>")
                    .appendTo(ul);
            }
            return $("<li></li>")
                .data("item.autocomplete", item)
                .append("<a><i>" + item.label + "</i></a>")
                .appendTo(ul);
        };
    }
    this.enable_ajax = enable_ajax;
};

