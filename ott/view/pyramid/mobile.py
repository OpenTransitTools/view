import logging
log = logging.getLogger(__file__)

from pyramid.view import view_config

@view_config(route_name='stop_mobile', renderer='mobile/stop.html')
@view_config(route_name='stop_mobile_short', renderer='mobile/stop.html')
def stop(request):
    stop   = request.model.get_stop(request.query_string, **request.params)
    ret_val = {}
    ret_val['stop'] = stop
    return ret_val

@view_config(route_name='stop_select_form_mobile', renderer='mobile/stop_select_form.html')
@view_config(route_name='stop_select_form_mobile_short', renderer='mobile/stop_select_form.html')
def stop_select_form(request):
    ret_val = {}
    ret_val['place']  = html_utils.get_first_param(request, 'place')
    ret_val['routes'] = request.model.get_routes(request.query_string, **request.params)
    return ret_val
