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
    function add(label, lat, lon)
    {
        try
        {
            if(label)
            {
                var db  = this.get_store({});
                var rec = this.make_record(label, lat, lon, true);
                if(db && rec)
                {
                    db[label] = rec;
                    localStorage.setItem(this.DB_NAME, JSON.stringify(db));
                }
            }
        } catch(e) {
            console.log(e);
        }
    }
    this.add = add;

    function add_solr_rec(item)
    {
        try
        {
            this.add(item.label, item.solr_doc.lat, item.solr_doc.lon);
        } catch(e) {
            console.log(e);
        }
    }
    this.add_solr_rec = add_solr_rec;


   /**
    * hide list element with matching label with 'remove' text
    * and remove the saved search from localStorage
    */
    function remove(label)
    {
        $("li:contains(" + label + ")").has('span:contains(' + this.removeTitle + ')').hide();
        var db = this.get_store();
        if(db)
        {
            delete db[label];
            localStorage.setItem(this.DB_NAME, JSON.stringify(db));
        }
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
            var db = this.get_store();
            if(db)
            {
                  term = term.trim().toUpperCase();

                //check that saved search terms match current search term
                for(var key in db)
                {
                    if(db.hasOwnProperty(key) && 
                       key.toUpperCase().indexOf(term) >= 0)
                    {
                        ret_val.push(db[key]);
                    }
                }
            }
        }
        catch(e) {
            console.log(e);
        }
        return ret_val;
    }
    this.find = find;

    /**
     * returns either the existing store, or create a new store in localStorage
     */
    function get_store(def_val)
    {
        var ret_val = def_val;
        var existing_store = localStorage.getItem(this.DB_NAME);
        if (existing_store !== null)
            ret_val = JSON.parse(existing_store);
        return ret_val; 
    }
    this.get_store = get_store;

    /**
     * makes a new record for our store...
     */
    function make_record(label, lat, lon, saved)
    {
        var ret_val = null;
        if(label)
        {
            var rec = {};
            rec['label'] = label;
            if(lat)   rec['lat'] = lat;
            if(lon)   rec['lon'] = lon;
            if(saved) rec['saved'] = true;
            ret_val = rec;
        }
        return ret_val;
    }
    this.make_record = make_record;

    /** 
     * makes a list item for each solr record...
     * such records have callbacks to remove the item from the list (see onClick below)
     */
    function make_list_item(item)
    {
        var THIS = this;

        // step 1: add an onClick callback to add this item to our store
        var a = document.createElement("a");
        a.onclick = function(e) {
            THIS.add_solr_rec(item);
        }

        // step 2: add the 'remove' crap...
        if(item.saved)
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
        else
        {
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
            console.log(e);
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

