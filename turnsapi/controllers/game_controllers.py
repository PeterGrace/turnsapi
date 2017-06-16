from pyramid.httpexceptions import HTTPFound
from turnsapi.models.basic import DBSession
from turnsapi.models.OAuthModel import OAuthModel
from turnsapi.models.game_models import Player, Game
from sqlalchemy.orm.exc import NoResultFound
import logging
from turnsapi.controllers.game_logic import GameLogic

def initialize_game(player):
    game = Game()
    game.player = player.id
    game.turns = 100
    game.lands = 1
    game.serfs = 10
    game.gold = 100
    game.granaries = 100
    DBSession.add(game)
    return {'turns': game.turns, 'lands': game.lands, 'serfs': game.serfs, 'gold': game.gold, 'granaries': game.granaries} 

def get_current_turn(player):
    try:
        game = DBSession.query(Game).filter(Player.id==player.id).one()
        return {'turns': game.turns, 'lands': game.lands, 'serfs': game.serfs, 'gold': game.gold, 'granaries': game.granaries} 
    except NoResultFound:
        logging.warn("User did not have a game, we'll start one for them.")
        return initialize_game(player)

def post_turn(request):
    login = request.user()
    if isinstance(login,HTTPFound):
        raise login
    if login is None:
        return HTTPBadRequest("you must be logged in.")
    player = login.player
    try:
        game = DBSession.query(Game).filter(Player.id==player.id).one()
    except NoResultFound:
        logging.warn("User did not have a game, we'll start one for them.")
        initialize_game(player)
        game = DBSession.query(Game).filter(Player.id==player.id).one()

    gl = GameLogic(game)
    gl.run_turn()

    game.turns -= 1
    game.lands = gl.lands
    game.serfs = gl.serfs
    game.gold = gl.gold
    game.granaries = gl.granaries
    return {'turns': game.turns, 'lands': game.lands, 'serfs': game.serfs, 'gold': game.gold, 'granaries': game.granaries} 

