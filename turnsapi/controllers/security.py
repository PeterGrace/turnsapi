from pyramid.security import authenticated_userid
from turnsapi.models.basic import (Base,DBSession)
from turnsapi.models.OAuthModel import OAuthModel
from sqlalchemy.orm.exc import NoResultFound
from pyramid.decorator import reify
import logging

def LookupUser(request):
  userid=authenticated_userid(request)
  try:
    logging.debug("Looking up user session for %s", userid)
    UserObject = DBSession.query(OAuthModel).filter(OAuthModel.email==userid).one()
    return UserObject
  except NoResultFound:
    return None

AccessLevels = {
   -1: "invalid",
   0: "unregistered",
   1: "g:user",
   2: "g:admin",
}

def groupfinder(userid,request):
  try:
    user = DBSession.query(OAuthModel).filter(OAuthModel.email==userid).one()
    if user is not None:
        return AccessLevels[user.AccessLevel]
  except NoResultFound:
    return None

