<%namespace name="util"  file="/shared/utils.mako"/>
<%def name="help_english()">
        <!-- GeoCoder TIPS (should include localized version of this some way / shape / form) -->
        <h3>If the trip planner fails to find a location:</h3>
        
        <h4>Check your spelling</h4>
        <p>If the trip planner cannot find an exact match on the spelling of a street or landmark, it will show you a list of alternatives, but if it finds a match, it will only show you the one that matches, which may not be the one you intended.</p>
        <blockquote>For example, if you type <kbd>400 Hawthourn</kbd> it will show you a list of alternatives that includes <kbd>400 SE Hawthorne Blvd.</kbd>, but if you type <kbd>400 Hawthorn</kbd> it will only find <kbd>400 SW Hawthorn Rd. (in Estacada)</kbd>.</blockquote>
        
        <p>Don't spell out directions, such as <kbd>North</kbd> or <kbd>Northwest</kbd> unless they are part of a street or landmark name (such as <kbd>SW North Ave</kbd> or <kbd>Northwest Senior Center</kbd>). Use abbreviations instead.</p>
        <blockquote>For example: Use <kbd>SE Hawthorne</kbd> <b>not</b> <kbd>Southeast Hawthorne</kbd></blockquote>
            
        <p>You may need to spell out the street name. Not all abbreviations are known to the trip planner. It knows that <kbd>MLK</kbd> means <kbd>Martin Luther King Jr. Blvd.</kbd> but it will not find <kbd>Hwy 99</kbd>.</p>
        
        <h4>The address may not exist.</h4>
        <p>If you've entered an address, try using an intersection instead.</p>
        
        <h4>The address may be confused with another.</h4>
        <p>Addresses that start with zero confuse the trip planner. It will find both <kbd>049 SW Porter</kbd> and <kbd>49 SW Porter</kbd> if you enter either address, but both will be listed as <kbd>49 SW PORTER ST</kbd>. Use a nearby intersection instead, such as <kbd>SW 1st & Porter</kbd> or <kbd>Naito Parkway & Porter</kbd>.</p>
        
        <h4>New streets or developments.</h4>
        <p>If the street or address is new, the trip planner may not know it yet. Try another  address or intersection that is near to the one you're trying to find.</p>
        
        <h4>New street names.</h4>
        <p>Some streets have been renamed. For example, <kbd>Martin Luther King Jr. Blvd.</kbd> used to be named <kbd>Union Ave.</kbd>, and <kbd>Naito Parkway</kbd> was named <kbd>Front Ave</kbd>.</p>
</%def>
<%def name="help_spanish()">
        <!-- SPANISH help slideout -->
        <!-- GeoCoder TIPS (should include localized version of this some way / shape / form) -->
        <h3>SPANISH - If the trip planner fails to find a location:</h3>
        
        <h4>Check your spelling</h4>
        <p>If the trip planner cannot find an exact match on the spelling of a street or landmark, it will show you a list of alternatives, but if it finds a match, it will only show you the one that matches, which may not be the one you intended.</p>
        <blockquote>For example, if you type <kbd>400 Hawthourn</kbd> it will show you a list of alternatives that includes <kbd>400 SE Hawthorne Blvd.</kbd>, but if you type <kbd>400 Hawthorn</kbd> it will only find <kbd>400 SW Hawthorn Rd. (in Estacada)</kbd>.</blockquote>
        
        <p>Don't spell out directions, such as <kbd>North</kbd> or <kbd>Northwest</kbd> unless they are part of a street or landmark name (such as <kbd>SW North Ave</kbd> or <kbd>Northwest Senior Center</kbd>). Use abbreviations instead.</p>
        <blockquote>For example: Use <kbd>SE Hawthorne</kbd> <b>not</b> <kbd>Southeast Hawthorne</kbd></blockquote>
            
        <p>You may need to spell out the street name. Not all abbreviations are known to the trip planner. It knows that <kbd>MLK</kbd> means <kbd>Martin Luther King Jr. Blvd.</kbd> but it will not find <kbd>Hwy 99</kbd>.</p>
        
        <h4>The address may not exist.</h4>
        <p>If you've entered an address, try using an intersection instead.</p>
        
        <h4>The address may be confused with another.</h4>
        <p>Addresses that start with zero confuse the trip planner. It will find both <kbd>049 SW Porter</kbd> and <kbd>49 SW Porter</kbd> if you enter either address, but both will be listed as <kbd>49 SW PORTER ST</kbd>. Use a nearby intersection instead, such as <kbd>SW 1st & Porter</kbd> or <kbd>Naito Parkway & Porter</kbd>.</p>
        
        <h4>New streets or developments.</h4>
        <p>If the street or address is new, the trip planner may not know it yet. Try another  address or intersection that is near to the one you're trying to find.</p>
        
        <h4>New street names.</h4>
        <p>Some streets have been renamed. For example, <kbd>Martin Luther King Jr. Blvd.</kbd> used to be named <kbd>Union Ave.</kbd>, and <kbd>Naito Parkway</kbd> was named <kbd>Front Ave</kbd>.</p>
</%def>

<%def name="geocode_highslide()">
    <!-- help highslide -->
    <div class="highslide-html-content" id="highslide-help" style="width:700px;">
        <div class="highslide-header">
            <ul>
                <li class="highslide-move"><a href="#" onClick="return false">$(_{u'Move')}</a></li>
                <li class="highslide-close"><a href="#" onClick="return hs.close(this)">$(_{u'Close')}</a></li>
            </ul>
        </div>
        <div class="highslide-body" style="text-align:left;">
            <% loc = util.get_locale() %>  
            %if loc == 'es':
                ${help_spanish()}
            %else:
                ${help_english()}
            %endif
            <p align="center"><a href="#" onClick="return hs.close(this)">$(_{u'Close')}</a></p>
        </div>
    </div>
</%def>

<%def name="form_help_right()">
<p class="help"><small>${_(u'Address, intersection, landmark or Stop ID')}</small></p>
</%def>

