from pyramid.httpexceptions import HTTPFound
from turnsapi.models.basic import DBSession
from turnsapi.models.OAuthModel import OAuthModel
from turnsapi.models.game_models import Player, Game
from sqlalchemy.orm.exc import NoResultFound
import logging
from turnsapi.controllers.game_logic import GameLogic, EndGameException

def return_status(player_id, messages=[]):
    try:
        game = DBSession.query(Game).filter(Player.id==player_id).one()
    except NoResultFound:
        return {}

    status = {
        'food': game.food,
        'player': game.player,
        'turns': game.turns,
        'lands': game.lands,
        'serfs': game.serfs,
        'gold': game.gold,
        'granaries': game.granaries,
        'messages': messages
    }
    return status


def initialize_game(player):
    game = Game()
    game.player = player.id
    game.turns = 100
    game.lands = 1
    game.serfs = 10
    game.gold = 100
    game.granaries = 1
    game.food = 10000
    game.taxrate = 5
    DBSession.add(game)
    return return_status(player.id)

def get_current_turn(player):
    try:
        game = DBSession.query(Game).filter(Player.id==player.id).one()
        return return_status(game)
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

    logging.info("POSTS: {}".format(request.POST))
    if 'discover' in request.POST:
        gl.do_discovery()


    try:
        gl.run_turn()
    except EndGameException:    
        DBSession.delete(game)
        logging.info("Player died, deleting their game.")
        return {"message": "Game over."}


    game.turns -= 1
    game.lands = gl.lands
    game.serfs = gl.serfs
    game.gold = gl.gold
    game.food = gl.food
    game.taxrate = gl.taxrate
    game.granaries = gl.granaries
    DBSession.flush()
    return return_status(player.id, gl.messages)

