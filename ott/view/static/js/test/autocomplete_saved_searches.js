if(window.console == undefined) window.console = {};
if(window.console.log == undefined) window.console.log = function(el){};

/**
 * data structs for storing place data... 
 */
function PlaceDAO(label, lat, lon, saved)
{
    this.label = null;
    this.lat   = null;
    this.lon   = null;
    this.saved = false;
    this.city  = null;
    this.type  = null;

    this.set = function(label, lat, lon, saved, city, type)
    {
        this.label = label;
        this.lat   = lat;
        this.lon   = lon;
        this.saved = saved;
        this.city  = city;
        this.type  = type;
    };

    this.copy = function()
    {
        var ret_val = new PlaceDAO();
        ret_val.set(this.label, this.lat, this.lon, this.saved, this.city, this.type);
        return ret_val;
    };

    if(label)
        this.set(label, lat, lon, saved);
}

/** extended data and functionality for SOLR*/
function SolrPlaceDAO(doc, saved)
{
    /** 
     * function that controls the naming of the geo point
     * NOTE: this isn't localized (e.g., type name and city conjunction), so override in .mako
     *
     * @return: formatted place name, ala 844 SE X Street, Portland -or- A Ave, Portalnd (Stop ID 2)  
     */
    this.place_name_format = function(doc)
    {
        var ret_val = doc.name;
        try {
            var city = '';
            if (doc.city && doc.city.length > 0)
               city = ", " + doc.city;

            var id = doc.id;
            if (doc.type == 'stop')
                id = doc.stop_id;

            var stop = '';
            if(doc.type == 'stop')
                stop = " (Stop ID " + id + ")";
            ret_val = doc.name + city + stop;
        }
        catch(e) {
            console.log(e);
        }
        return ret_val;
    };

    var label = this.place_name_format(doc);
    this.set(label, doc.lat, doc.lon, saved, doc.city, doc.type);
}
SolrPlaceDAO.prototype = new PlaceDAO();


/**
 * PlaceCache is a local store caching system for PlaceDAO records...

 * @param {Object} removeTitle is the 'name' of the remove (from store) link ... defaults to 'remove'  
 * @param {Object} saveOnClick means that when a result from the auto-complete list is clicked, it will get saved into the cache
 */
function PlaceCache(removeTitle, saveOnClick)
{
    this.removeTitle = removeTitle || 'remove';
    this.saveOnClick = saveOnClick;
    this.DB_NAME = 'searchTerms';

    /**
     * add an item to our local store
     */
    this.add = function(rec)
    {
        try
        {
            if(rec && rec.label)
            {
                var db  = this.get_store({});
                if(db)
                {
                    rec.saved = true;
                    db[rec.label] = rec;
                    localStorage.setItem(this.DB_NAME, JSON.stringify(db));
                }
            }
        } catch(e) {
            console.log(e);
        }
    };


   /**
    * hide list element with matching label with 'remove' text
    * and remove the saved search from localStorage
    */
    this.remove = function(label)
    {
        $("li:contains(" + label + ")").has('span:contains(' + this.removeTitle + ')').hide();
        var db = this.get_store();
        if(db)
        {
            delete db[label];
            localStorage.setItem(this.DB_NAME, JSON.stringify(db));
        }
    };


    /**
     * find all matching terms in local store, and return them... 
     */
    this.find = function(term)
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
    };

    /**
     * returns either the existing store, or create a new store in localStorage
     */
    this.get_store = function(def_val)
    {
        var ret_val = def_val;
        var existing_store = localStorage.getItem(this.DB_NAME);
        if (existing_store !== null)
            ret_val = JSON.parse(existing_store);
        return ret_val; 
    };


    /** 
     * makes a list item for each solr record...
     * such records have callbacks to remove the item from the list (see onClick below)
     */
    this.make_list_item = function(item)
    {
        var THIS = this;

        // step 0: we're gonna wrap elements in an a tag...
        var a = document.createElement("a");

        // step 1: add an onClick callback to add this item to our store
        if(this.saveOnClick)
        {
            a.onclick = function(e) {
                if(item && !item.saved)
                {
                    var n = item.copy();
                    THIS.add(n);
                }
                return true;
            };
        }

        // step 2: is this is a cached item, add a 'remove' link to get it out of our cache
        if(item.saved)
        {
            a.innerHTML = '<b>' + item.label + '</b>';
            var span = document.createElement("span");
            span.setAttribute('class', 'remove');
            span.onclick = function(e) {
                THIS.remove(item.label);  // step 1: remove the cached item from our drop down
                e.stopPropagation();      // step 2: prevent the deleted item from selection (and keep drop down open)
                console.log("NOTE: stop propogation of select event...");
                return true;
            };
            span.innerHTML = this.removeTitle;
            a.appendChild(span);
        }
        else
        {
            a.innerHTML = item.label;
        }
        return a;
    };
}


/**
 * SOLRAutoComplete class that will call SOLR, and return text data...
 * new SOLRAutoComplete('#input_div_id')
 * 
 * @param {Object} input_div is the div id that we attach to autocorrect ('#input' is the default)
 * @param {Object} solr_url is the path to solr's select service (localhost/solr/select by default)
 * @param {Object} remove_title is the label on the 'remove' link in the drop-down list of cached results ('remove' by default)
 * @param {Object} save_on_click will put any item that's clicked/selected from the drop-down into the cache (false by default)
 * @param {Object} num_results is the number of solr results to return (6 by default) 
 */
function SOLRAutoComplete(input_div, solr_url, cache, num_results)
{
    this.input_div   = input_div   || "#input";
    this.solr_url    = solr_url    || "http://127.0.0.1/solr/select";
    this.num_results = num_results || "6";
    this.cache       = cache;


    /** callback (that you override) to get the resulting clicked SOLR document */
    this.select_callback = function(sel)
    {
        console.log('Selected:' + sel + " " + this.solr_url);
        return true;
    };


    this.enable_ajax = function()
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

                        // step 1: get cached searches
                        if(THIS.cache)
                        {
                            var save_list = THIS.cache.find(request.term);
                            //data.concat(save_list);
                            data = save_list;
                        }

                        // step 2: SOLR elements...
                        docs = resp.response.docs;
                        len = docs.length;

                        // step 3: loop through SOLR results, and build data object required for jQ's autocomplete 
                        for(var i = 0; i < len; i++)
                        {
                            var dao = new SolrPlaceDAO(docs[i]);
                            data.push(dao);
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
                    console.log("ERROR: SOLRAutoComplete - select callback: " + e); 
                }
                return true;
            }

        // set custom display for autocomplete results
        // render saved search terms with a 'remove' span
        }).data("ui-autocomplete")._renderItem = function(ul, item) {

            // step 1: either make a 'cache'-able list element, or just normal element
            var elem;
            if(THIS.cache)
            {
                elem = THIS.cache.make_list_item(item);
            }
            else
            {
                elem = document.createElement("a");
                elem.innerHTML = item.label;
            }

            // step 2: add this element to the drop down list...
            var ret_val = $("<li style='position:relative'></li>")
                        .data("item.autocomplete", item)
                        .append(elem)
                        .appendTo(ul);

            return ret_val;
        };
    };
};

