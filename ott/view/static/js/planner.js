function expandMe(me)
{
    var node = me.parentNode.className;
    if(node.indexOf(' expanded') > 0)
    {
        me.parentNode.className = node.replace(' expanded', '');
        console.log('contract');
    }
    else 
    {
        me.parentNode.className = node + ' expanded';
        console.log('expand');
    }

    return false;
}

var desc_el = null;

function show_hide_el(el, cmd)
{
    if(el && el.style)
        el.style.display = cmd;
}


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

function show(id)
{
    var el = document.getElementById('desc_' + id);
    var same_selection = (el == desc_el) ? 'True' : 'False';
    var init_selection = (el.style.display == '') ? 'True' : 'False';
    var el_none = (el.style.display == 'none') ? 'True' : 'False';
    var el_block = (el.style.display == 'block') ? 'True' : 'False';

    // the line below will collapse the open description column from the page.
    // the value of the global desc_el is from the previous row selection.
    show_hide_el(desc_el, 'none');

    var doShow = false;

    if (el_none == 'True' || init_selection == 'True') {
        // the selection is collapsed, so expand it.
        show_hide_el(el, 'block');
        doShow = true;
    }
    if (el_block == 'True' && same_selection == 'True') {
        // the selection is collapsed, so expand it.
        show_hide_el(el, 'none');
    }
    // Since the current row could have been changed from block to none,
    // This if then statement will insure that it remains block.  It will
    // appear to not toggle.
    if (el_none == 'True' && same_selection == 'True') {
        show_hide_el(el, 'block');
        doShow = true;
    }

    if(doShow) {
        dynamiclyLoadImages(el)
    }

    desc_el = el;
}
