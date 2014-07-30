/**
 @copy: TriMet 2013
 @auth: Frank Purcell
 **/

var DEF_IMG_WIDTH=100;
var DEF_IMG_HEIGHT=100;
if(window.console == undefined) window.console = {};
if(window.console.log == undefined) window.console.log = function(el){};


/** load an img dynamically as opposed on page load time
    via this img tag:
 */
function dynamiclyLoadImages(el)
{
    try
    {
        var img_list = el.getElementsByTagName('img');
        for(var i in img_list)
        {
            var img = img_list[i];
            // make sure we are dealing with an img tag, and only call it once (don't need to reload same img over & over)
            if(img && img.src && img.attributes.dsrc && img.src.indexOf(img.attributes.dsrc.value) < 0)
            {
                img.src    = img.attributes.dsrc.value;
                img.width  = img.attributes.dwidth  ? img.attributes.dwidth.value  : DEF_IMG_WIDTH;
                img.height = img.attributes.dheight ? img.attributes.dheight.value : DEF_IMG_HEIGHT;
                console.log(img.src)
            }
        }
    }
    catch(e)
    {}
}


/** 
 * related to the dynamic image stuff ... this is a show / hide <div> method...
 * shows where to call the dynamicLoadImages method 
 */
function expandMe(me)
{
    var node = me.parentNode.className;
    if(node.indexOf(' expanded') > 0)
    {
        me.parentNode.className = node.replace(' expanded', '');
        console.log('contract');
        me.className = 'open';
    }
    else
    {
        me.parentNode.className = node + ' expanded';
        console.log('expand');
        me.className = 'close';
        dynamiclyLoadImages(me.parentNode);
    }
    return false;
}

