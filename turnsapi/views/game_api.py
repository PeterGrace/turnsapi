from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from cornice import Service
import logging

from turnsapi.controllers.game_controllers import get_current_turn, post_turn

turn = Service(name='turn', description = 'game tasks', path='/turn/status')

@turn.get()
def turn_get(request):
    login = request.user()
    if isinstance(login,HTTPFound):
        raise login
    if login is None:
        return HTTPBadRequest("you must be logged in.")
    user = login.player
    return get_current_turn(user)

@turn.post()
def turn_post(request):
    return post_turn(request)
