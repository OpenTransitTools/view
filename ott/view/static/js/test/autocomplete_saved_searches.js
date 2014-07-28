if(window.console == undefined) window.console = {};
if(window.console.log == undefined) window.console = function(el){};

/** 
 * SavedSearch
 */
function SavedSearches(removeTitle)
{
    this.removeTitle = removeTitle || 'remove';
    this.DB_NAME = 'searchTerms';

    /** 
     * add an item to our local store
     */
    function add(item)
    {
        try
        {
            var searchT = {};
            var searchT_raw = localStorage.getItem(this.DB_NAME);
            if (searchT_raw !== null)
            {
                searchT = JSON.parse(searchT_raw);
            }
            item["saved"] = true;
            searchT[item.label] = item;
            localStorage.setItem(this.DB_NAME, JSON.stringify(searchT));
        } catch(e) {}
    }
    this.add = add;

   /**
    * hide list element with matching label with 'remove' text
    * and remove the saved search from localStorage
    */
    function remove(label)
    {
        $("li:contains(" + label + ")").has('span:contains(' + this.removeTitle + ')').hide();
        var searchT_raw = localStorage.getItem(this.DB_NAME);
        var searchT = JSON.parse(searchT_raw);
        delete searchT[label];
        localStorage.setItem(this.DB_NAME, JSON.stringify(searchT));
    }
    this.remove = remove;

    /**
     * find all matching terms in local store, and return them... 
     */
    function find(term)
    {
        var ret_val = [];
        try 
        {
            var searchT_raw = localStorage.getItem(this.DB_NAME);
            if (searchT_raw !== null)
            {
                var searchT = JSON.parse(searchT_raw);
                term = term.trim().toUpperCase();

                //check that saved search terms match current search term
                for (var key in searchT)
                {
                    if (searchT.hasOwnProperty(key) && 
                        key.toUpperCase().indexOf(term) >= 0)
                    {
                        ret_val.push(searchT[key]);
                    }
                }
            }
        } catch(e) {}
        return ret_val;
    }
    this.find = find;

    function make_list_item(item)
    {
        var THIS = this;

        var a = document.createElement("a");
        a.onclick = function(e) {
            THIS.add(item);
        }

        if (item.saved)
        {
            a.innerHTML = '<b>' + item.label + '</b>';
            var span = document.createElement("span");
            span.setAttribute('class', 'remove');
            span.onclick = function(e) {
                THIS.remove(item.label);
                e.stopPropagation();  // prevent selection (and keep drop down open)
            }
            span.innerHTML = this.removeTitle;
            a.appendChild(span);
        }
        else {
            a.innerHTML = item.label;
        }
        return a;
    }
    this.make_list_item = make_list_item;
}


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
    this.saved       = new SavedSearches('la áqui');


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
            var stop = '';
            if(type == 'stop')
                stop = " (Stop ID " + id + ")";
            ret_val = name + city + stop;
        }
        catch(e) {
        }
        return ret_val;
    }
    this.place_name_format = place_name_format;


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
                        //push saved searchings 
                        var data = [];

                        var save_list = THIS.saved.find(request.term);
                        //data.concat(save_list);
                        data = save_list;

                        // step 0: SOLR elements...
                        docs = resp.response.docs;
                        len = docs.length;

                        // step 1: loop through SOLR results, and build data object required for jQ's autocomplete 

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
        // render saved search terms with a 'remove' span
        }).data("ui-autocomplete")._renderItem = function(ul, item) {

            return $("<li style='position:relative'></li>")
                    .data("item.autocomplete", item)
                    .append(THIS.saved.make_list_item(item))
                    .appendTo(ul);
        };
    }
    this.enable_ajax = enable_ajax;
};

