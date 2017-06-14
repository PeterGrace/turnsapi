from pyramid.response import Response
from pyramid.view import view_config


from turnsapi.models.basic import (
    DBSession,
    )

@view_config(route_name='home', renderer='turnsapi:templates/home.mak')
def view_home(request):
    return({"key":"value"})
