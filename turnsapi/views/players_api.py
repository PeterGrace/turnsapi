from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest
from cornice.resource import resource

from turnsapi.controllers.player_controllers import get_player_data


@resource(collection_path='/players', path='/players/{id}')
class PlayerAPI(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        return { 'players': None}

    def get(self):
        if 'id' in self.request.matchdict:
            try:
                id = int(self.request.matchdict['id'])
                return get_player_data(id)
            except ValueError:
                return HTTPBadRequest("Invalid ID provided.")
