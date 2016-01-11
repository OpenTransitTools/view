/** text_planner.js is mostly a wrapper library
**/
if(window.console == undefined) window.console = {};
if(window.console.log == undefined) window.console.log = function(el){};

function tpShowTimeControls(form) {
    try {
        showTimeControls(form.selectedIndex);
    } catch(e) {
        console.log(e);
    }
}

function tpDoText(form, content) {
    try {
        doText(form, content);
    } catch(e) {
        console.log(e);
    }
}

function tpDoClassRegular(form) {
    try {
        doClassRegular(form);
    } catch(e) {
        console.log(e);
    }
}

function tpGoogleAnalytics(ga, content)
{
    try {
        ga.push(content);
    } catch(e) {
        console.log(e);
    }
}

// THESE doX functions are from old trimet.org/basic.js (removed in 2016)
// form highlighting and text replacement
function doClear(thisfield, defaulttext) {
    thisfield.className='highlight';
    if (thisfield.value == thisfield.defaultValue) {
	thisfield.value = "";
    }
}
function doText(thisfield, defaulttext) {
    if (thisfield.value == "") {
	thisfield.value = thisfield.defaultValue;
	thisfield.className='regular';
    }
    else {
	thisfield.className='regular-complete';
    }
}
function doClassHighlight(thisfield) {
    thisfield.className='highlight';
}
function doClassRegular(thisfield) {
    thisfield.className='regular';
}

