from pyramid.view import view_config

@view_config(route_name='stop_desktop', renderer='desktop/stop.html')
def stop(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    ret_val['stop'] = request.model.get_stop()

    return ret_val


@view_config(route_name='find_stop_desktop', renderer='desktop/find_stop.html')
def find_stop(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    ret_val['routes'] = request.model.get_routes()['routes']

    return ret_val


@view_config(route_name='tracker_desktop', renderer='desktop/tracker.html')
def tracker(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    ret_val['routes'] = request.model.get_routes()['routes']

    return ret_val
