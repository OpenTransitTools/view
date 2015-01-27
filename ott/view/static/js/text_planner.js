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