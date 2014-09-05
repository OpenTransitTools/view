###
### IMPORTANT !!!!!!!!!!!!!!!
### TODO ... not sure this is used 
### 

steps = [
{
    'name':None,        # from place / to place / step name / elevator
    'conjunction':None, # from, to, on
    'dir':{'name':None, 'compass':None, 'raw':None, 'img':None},
    'mode':None,        # Walk, Bike, Drive, Fly
    'distance':None,
    'elevation':{'start':None, 'end':None, 'trend':None},
    
}
]

#### NOTE ... not used?
<%def name="render_steps(verb, frm, to, steps)">
</%def>

<%def name="Xrender_steps(verb, frm, to, steps)">
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


