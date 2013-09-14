from pyramid.view import view_config

@view_config(route_name='stop_select_form_mobile', renderer='mobile/stop_select_form.html')
def stop_select_form(request):
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
