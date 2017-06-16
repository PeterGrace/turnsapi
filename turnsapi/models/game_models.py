from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
    )
from sqlalchemy.orm import relationship

from turnsapi.models.basic import Base

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    logins = relationship("OAuthModel", back_populates="player")


class Game(Base):
    __tablename__ = 'game_data'
    id = Column(Integer, primary_key=True)
    player = Column(Integer, ForeignKey('players.id'), nullable=False)
    food = Column(Integer, nullable=False)
    turns = Column(Integer, nullable=False)
    lands = Column(Integer, nullable=False)
    serfs = Column(Integer, nullable=False)
    gold = Column(Integer, nullable=False)
    granaries = Column(Integer, nullable=False)
