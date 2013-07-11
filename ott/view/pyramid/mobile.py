from pyramid.view import view_config

@view_config(route_name='find_stop_mobile', renderer='mobile/find_stop.html')
def find_stop(request):
    '''
    '''
    ret_val = {}
    ret_val['routes'] = request.model.get_routes()['routes']

    return ret_val


@view_config(route_name='stop_mobile', renderer='mobile/stop.html')
def stop(request):
    '''
    '''
    ret_val = {}
    ret_val['routes'] = request.model.get_routes()['routes']

    return ret_val
