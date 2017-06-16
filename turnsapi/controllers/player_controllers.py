from turnsapi.models.basic import DBSession
from turnsapi.models.game_models import Player

def get_player_data(id):
    rs = DBSession.query(Player).filter(Player.id == id).first()
    return rs
