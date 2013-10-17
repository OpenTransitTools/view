var DEF_IMG_WIDTH=100;
var DEF_IMG_HEIGHT=100;
if(window.console == undefined) window.console = {};
if(window.console.log == undefined) window.console = function(el){};

function dynamiclyLoadImages(el)
{
    try
    {
        var img_list = el.getElementsByTagName('img');
        for(var i in img_list)
        {
            var img = img_list[i];
            if(img && img.attributes.dsrc && img.src != img.attributes.dsrc.value)
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
