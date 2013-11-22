/**
 * 
 * @param {Object} input_div
 * @param {Object} log_div
 * @param {Object} solr_url
 */
function SOLRAutoComplete(input_div, num_results, solr_url) {
    this.input_div   = input_div   || "#input";
    this.num_results = num_results || "20";
    this.solr_url    = solr_url    || "http://maps5.trimet.org/solr/select";

    function select_callback(solr_doc)
    {
        console.log('Selected:' + solr_doc.value + ", id: " + solr_doc.id + " " + this.solr_url);
        
    }
    this.select_callback = select_callback;

    function enable_ajax()
    {
        var THIS = this;  // make SOLRAutoComplete instance 'this' available to jQuery ajax stuff below 

        $(THIS.input_div).autocomplete({
            minLength : 1,
            delay     : 500,
            source : function(request, response) {
                $.ajax({
                    type : "GET",
                    dataType : "json",
                    url : THIS.solr_url,
                    data : {
                        q : request.term,
                        wt : "json",
                        qt : "dismax",
                        rows : THIS.num_results
                    },
                    cache : false,
                    // jQuery ajax callback
                    success : function(resp, resp_code)
                    {
                        // step 0: SOLR elements...
                        docs = resp.response.docs;
                        len = docs.length;

                        // step 1: loop through SOLR results, and build data object required for jQ's autocomplete 
                        var data = [];
                        for (var i = 0; i < len; i++)
                        {
                            // step 2: make a label out of name and optionally city
                            var label = docs[i].name;
                            if (docs[i].city && docs[i].city.length > 0 && docs[i].city != 'undefined')
                                label = label + ", " + docs[i].city;

                            // step 3: make the autocomplete object, and add it to our return array
                            var s = {
                                "id" : docs[i].id,
                                "label" : label,
                                "value" : label,
                                "solr_doc" : docs[i]
                            };
                            data.push(s);
                        }
                        // step 4: jQuery UI autocomplete (required) callback
                        response(data);
                    }
                });
            },

            // jQuery autocomplete selected value callback
            select : function(event, ui)
            {
                THIS.select_callback(ui.item);
                
            }
        });
    }
    this.enable_ajax = enable_ajax;
};

