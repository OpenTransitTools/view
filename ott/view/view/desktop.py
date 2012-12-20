from pyramid.view import view_config

from ott.view.model import Model
from ott.view.model_mock import ModelMock
model = ModelMock()

@view_config(route_name='find_stop', renderer='desktop/stop.html')
def find_stop(request):
    '''
       what do i do?
       1. ...
       2. ...
    '''
    ret_val = {}
    ret_val['routes'] = model.get_routes()['routes']

    return ret_val
