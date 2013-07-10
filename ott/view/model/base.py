

class Base():

    TRAIN     = 'TRAIN'
    RAIL      = 'RAIL'
    STREETCAR = 'STREETCAR'
    TRAM      = 'TRAM'
    WALK      = 'WALK'
    GONDOLA   = 'GONDOLA'
    TRANSIT   = 'TRANSIT'
    BICYCLE   = 'BICYCLE'
    BIKE      =  BICYCLE


    def get_plan(self, get_params, **kwargs): pass

    def get_stop(self, get_params, **kwargs): pass
    def get_stop_schedule(self, get_params, **kwargs): pass

    def get_routes(self, get_params, **kwargs): pass
