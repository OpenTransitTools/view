from pyramid.view import view_config

@view_config(route_name='mfind_stop', renderer='mobile/stop.html')
def find_stop(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    ret_val['routes'] = model.get_routes()['routes']

    return ret_val
