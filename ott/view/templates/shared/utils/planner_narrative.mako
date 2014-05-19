steps = [
{
    'name':None,        # from place / to place / step name / elevator
    'conjunction':None, # from, to, on
    'dir':{'name':None, 'compass':None, 'raw':None, 'img':None},
    'mode':None,        # Walk, Bike, Drive, Fly
    'distance':None
    
}
]
<%def name="render_steps(verb, frm, to, steps)">
    <ol>
        %for i, s in enumerate(steps):
        <%
            name = s['name']
            conjunction = _(u'on')
            if name == '' and i == 0:
                name = frm
                conjunction = _(u'from')
            elif name == '' and i+1 == len(steps):
                name = to
                conjunction = _(u'to')

            instruct_verb = verb
            turn = None
            dir = s['relative_direction']
            if dir != None:
                dir = dir.lower().replace('_', ' ').strip()
                #print dir, _(dir), _(unicode(dir)), _('right'), _(u'right'), _('left'), _('slightly left')
                if dir not in ('continue'):
                    turn = _(u'Turn') + " " + _(dir) + " " + _(u'on') + " " + _(name)
                else:
                    instruct_verb = dir.title()

            instruct = _(instruct_verb) + " " + pretty_distance(s['distance']) + " " + _(s['compass_direction']) + " " + conjunction + " " + _(name)
        %>
        %if turn != None:
        <li>${turn}</li>
        %endif
        <li>${instruct}</li>
        %endfor
    </ol>
</%def>

##
## make bike / walk turn by turn narrative
##
<%def name="make_instruction_steps(steps, verb, leg_id)">
        var retVal = [];
        var isFirstStep = true;

        var stepNum = 1;
        for (var i = 0; i < steps.length; i++)
        {
            var step = steps[i];
            if (step.streetName == "street transit link")
            {
                // TODO: Include explicit instruction about entering/exiting transit station or stop?
                continue;
            }

            var text = this.addNarrativeToStep(step, verb, stepNum);
            var cfg = {id:legId + "-" + i, text:step.narrative, cls:'itiny-steps', iconCls:'itiny-step-icon', icon:step.iconURL, text:text, num:stepNum++, originalData:step};
            var node = new otp.planner.StepData(cfg);
            retVal.push(node);
        }

        return retVal;
</%def>

##
## * adds narrative and direction information to the step
## * NOTE: this method has an intentional side-effect of chaning @param step 
## *       (see below -- specifying 4th @param dontEditStep == true will avoid this)
##
<%def name="add_narrative_to_step(step, verb, step_num, dont_edit_step=False)">
        var stepText   = "<strong>" + stepNum + ".</strong> ";
        var iconURL  = null;

## <img src="images/directions/right.png"/>

        var relativeDirection = step.relativeDirection;
        if ((relativeDirection == null || stepNum == 1) && step.absoluteDirection != null)
        {
            var absoluteDirectionText = this.locale.directions[step.absoluteDirection.toLowerCase()];
            stepText += verb + ' <strong>' + absoluteDirectionText + '</strong> ' + this.locale.directions.on;
            iconURL = otp.util.ImagePathManagerUtils.getStepDirectionIcon();
            // console.log(step);
        }
        else 
        {
            relativeDirection = relativeDirection.toLowerCase();
            iconURL = otp.util.ImagePathManagerUtils.getStepDirectionIcon(relativeDirection);

            var directionText = otp.util.StringFormattingUtils.capitolize(this.locale.directions[relativeDirection]);

            if (relativeDirection == "continue")
            {
                stepText += directionText;
            }
            else if (relativeDirection == "elevator")
            {
              // elevators are handled differently because, in English
              // anyhow, you want to say 'exit at' or 'go to' not
              // 'elevator on'
              stepText += directionText;
            }
            else if (step.stayOn == true)
            {
                stepText += directionText + " " + this.locale.directions['to_continue'];
            }
            else
            {
                stepText += directionText;
                if (step.exit != null) {
                    stepText += " " + this.locale.ordinal_exit[step.exit] + " ";
                }
                stepText += " " + this.locale.directions['on'];
            }
        }
        stepText += ' <strong>' + step.streetName + '</strong>';

        // don't show distance for routes which have no distance (e.g. elevators)
        if (step.distance > 0) {
            stepText += ' - ' + otp.planner.Utils.prettyDistance(step.distance) + '';
        }

        // edit the step object (by default, unless otherwise told)
        if(!dontEditStep)
        {
            // SIDE EFFECT -- when param dontEditStep is null or false, we'll do the following side-effects to param step
            step.narrative  = stepText;
            step.iconURL    = iconURL;
            step.bubbleHTML = '<img src="' + iconURL + '"></img> ' + ' <strong>' + stepNum + '.</strong> ' + step.streetName;
            step.bubbleLen  = step.streetName.length + 3;
        }

        return stepText;
    }
</%def>

<%
'''

#<div class="x-tree-root-node"><li class="x-tree-node"><div ext:tree-node-id="1-from" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny magnify" unselectable="on"><span class="x-tree-node-indent"></span><img src="/images/ui/s.gif" class="x-tree-ec-icon x-tree-elbow"><img src="images/ui/s.gif" class="x-tree-node-icon x-tree-node-inline-icon start-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"></span></a><h4><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"></a><a href="javascript:void(0);">Start at</a> PDX</h4></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-0" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny magnify" unselectable="on"><span class="x-tree-node-indent"></span><img src="/images/ui/s.gif" class="x-tree-ec-icon x-tree-elbow"><img src="images/ui/trip/mode/tram.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-inline-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"></span></a><h4><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"></a><a href="javascript:void(0);">Rail</a> MAX Red Line  to City Center &amp; Beaverton TC</h4><p class="leg-info"><span class="time">5:04am</span> Depart Portland Int'l Airport MAX Station<br><span class="stopid">Stop ID 10579</span></p><div class="duration">51 minutes</div><p class="leg-info"><span class="time">5:55am</span> Arrive Washington Park MAX Station<br><span class="stopid">Stop ID 10121</span></p></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-1" class="x-tree-node-el x-unselectable itiny magnify x-tree-node-expanded" unselectable="on"><span class="x-tree-node-indent"></span><img src="/images/ui/s.gif" class="x-tree-ec-icon x-tree-elbow-minus"><img src="images/ui/trip/mode/walk.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-inline-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"></span></a><h4><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"></a><a href="javascript:void(0);">Walk </a> to Southwest Knights Boulevard</h4><p class="leg-info transfers">About 8 minutes - 0.3 mi</p></div><ul class="x-tree-node-ct" style=""><li class="x-tree-node"><div ext:tree-node-id="1-leg-1-0" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny-steps x-tree-selected" unselectable="on"><span class="x-tree-node-indent"><img src="/images/ui/s.gif" class="x-tree-elbow-line"></span><img src="/images/ui/s.gif" class="x-tree-ec-icon x-tree-elbow"><img src="images/ui/trip/directions/clear.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-step-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"><strong>1.</strong> Walk <strong>west</strong> on <strong>Washington Park MAX Platform (path)</strong> - 56 ft</span></a></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-1-1" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny-steps" unselectable="on"><span class="x-tree-node-indent"><img src="/images/ui/s.gif" class="x-tree-elbow-line"></span><img src="/images/ui/s.gif" class="x-tree-ec-icon x-tree-elbow"><img src="images/ui/trip/directions/left.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-step-icon" unselectable="on">
<a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"><strong>2.</strong> Left on <strong>Elevator</strong></span></a></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-1-2" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny-steps" unselectable="on">
<span class="x-tree-node-indent"><img src="/images/ui/s.gif" class="x-tree-elbow-line"></span><img src="/images/ui/s.gif" class="x-tree-ec-icon x-tree-elbow">
<img src="images/ui/trip/directions/elevator.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-step-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"><strong>3.</strong> Take elevator to <strong>1</strong></span></a></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-1-3" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny-steps" unselectable="on"><span class="x-tree-node-indent">
<img src="images/ui/trip/directions/continue.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-step-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"><strong>4.</strong> Continue on <strong>path</strong> - 0.1 mi</span></a></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-1-4" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny-steps" unselectable="on"><span class="x-tree-node-indent">
<img src="images/ui/trip/directions/left.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-step-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"><strong>5.</strong> Left on <strong>Southwest Knights Boulevard (sidewalk)</strong> - 116 ft</span></a></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-1-5" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny-steps" unselectable="on"><span class="x-tree-node-indent">
<img src="images/ui/trip/directions/slightly_right.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-step-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"><strong>6.</strong> Slight right on <strong>path</strong> - 8 ft</span></a></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-1-6" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny-steps" unselectable="on"><span class="x-tree-node-indent">
<img src="images/ui/trip/directions/right.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-step-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"><strong>7.</strong> Right on <strong>Southwest Zoo Road</strong> - 152 ft</span></a></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-leg-1-7" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny-steps" unselectable="on"><span class="x-tree-node-indent">
<img src="images/ui/trip/directions/left.png" class="x-tree-node-icon x-tree-node-inline-icon itiny-step-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"><strong>8.</strong> Left on <strong>Southwest Knights Boulevard</strong> - 0.1 mi</span></a></div><ul class="x-tree-node-ct" style=""></ul></li></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-to" class="x-tree-node-el x-tree-node-leaf x-unselectable itiny magnify" unselectable="on"><span class="x-tree-node-indent"></span>
<img src="/images/ui/s.gif" class="x-tree-ec-icon x-tree-elbow">
<img src="/images/ui/s.gif" class="x-tree-node-icon end-icon" unselectable="on"><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1"><span unselectable="on"></span></a><h4><a hidefocus="on" class="x-tree-node-anchor" href="javascript:void(0);" tabindex="1">
</a><a href="javascript: void;">End at</a> Southwest Knights Boulevard</h4></div><ul class="x-tree-node-ct" style=""></ul></li><li class="x-tree-node"><div ext:tree-node-id="1-trip" class="x-tree-node-el x-tree-node-leaf x-unselectable trip-details-shell" unselectable="on"><span class="x-tree-node-indent"></span>
<img src="/images/ui/s.gif" class="x-tree-ec-icon x-tree-elbow-end">

    instructions :
    {
        walk         : "Walk",
        walk_toward  : "Walk",
        walk_verb    : "Walk",
        bike         : "Bike",
        bike_toward  : "Bike",
        bike_verb    : "Bike",
        drive        : "Drive",
        drive_toward : "Drive",
        drive_verb   : "Drive",
        move         : "Proceed",
        move_toward  : "Proceed",

        transfer     : "transfer",
        transfers    : "transfers",

        continue_as  : "Continues as",
        stay_aboard  : "stay on board",

        depart       : "Depart",
        arrive       : "Arrive",

        start_at     : "Start at",
        end_at       : "End at"
    },

                var template = 'TP_WALK_LEG';
                if (mode === 'walk') {
                    verb = this.locale.instructions.walk_toward;
                }
                else if (mode === 'bicycle') {
                    verb = this.locale.instructions.bike_toward;
                    template = 'TP_BICYCLE_LEG';
                    containsBikeMode = true;
                } else if (mode === 'car') {
                    verb = this.locale.instructions.drive_toward;
                    template = 'TP_CAR_LEG';
                    containsDriveMode = true;
                } else {
                    verb = this.locale.instructions.move_toward;
                }
                if (!leg.data.formattedSteps)
                {
                    instructions = this.makeInstructionStepsNodes(leg.data.steps, verb, legId, this.dontEditStep);
                    if(instructions && instructions.length >= 1)
                        isLeaf = false;
                    leg.data.formattedSteps = "";
                }
                text = this.templates[template].applyTemplate(leg.data);
'''
%>
