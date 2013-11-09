<!--
// Basic TriMet Javascript

/* not used currently */
function closeGlobalAlert() {
	document.getElementById("global-alert").className = "visuallyhidden";
}

// facebook script
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));


// google analytics	
var _gaq=[['_setAccount','UA-688646-3'],['_trackPageview']];
(function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
g.src=('https:'==location.protocol?'//ssl':'//www')+'.google-analytics.com/ga.js';
s.parentNode.insertBefore(g,s)}(document,'script'));


function openPopup(theURL,winName,features) { //v2.0
  tracker = window.open(theURL,winName,features);
  tracker.focus();
}

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



function MM_jumpMenu(targ,selObj,restore){ //v3.0
  eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'");
  if (restore) selObj.selectedIndex=0;
}


// for showing/hiding elements
function show_element(id) {
   var e = document.getElementById(id);
   e.style.display = 'block';
}
function hide_element(id) {
   var e = document.getElementById(id);
   e.style.display = 'none';
}
	// maybe don't need this now?
	function MM_showHideLayers() { //v6.0
	  var i,p,v,obj,args=MM_showHideLayers.arguments;
	  for (i=0; i<(args.length-2); i+=3) if ((obj=MM_findObj(args[i]))!=null) { v=args[i+2];
		if (obj.style) { obj=obj.style; v=(v=='show')?'visible':(v=='hide')?'hidden':v; }
		obj.visibility=v; }
	}


function HandleBodyOnClick() {
}
function HideAllMenus() {
}
function HideAllMenus() {
}


function go() {
	location=document.routes.path_suffix.
	options[document.routes.path_suffix.selectedIndex].value
}

// -->