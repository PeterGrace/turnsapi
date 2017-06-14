from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
    )
from sqlalchemy.orm import relationship
from turnsapi.models.basic import Base

class OAuthModel(Base):
    __tablename__ = 'oauth_creds'
    id = Column(Integer, primary_key=True)
    email = Column(Text,unique=True)
    AccessLevel = Column(Integer)
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship("Player", back_populates="logins")

Index('EmailIndex', OAuthModel.email, unique=True, mysql_length=255)

