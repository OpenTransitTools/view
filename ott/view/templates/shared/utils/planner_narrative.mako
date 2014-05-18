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



