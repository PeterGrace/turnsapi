from pyramid.security import authenticated_userid, unauthenticated_userid, remember
from turnsapi.models.basic import (Base,DBSession)
from turnsapi.models.OAuthModel import OAuthModel
from sqlalchemy.orm.exc import NoResultFound
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
import logging
import requests

def LookupUser(request):
  userid=authenticated_userid(request)
  try:
    logging.debug("Looking up user session for %s", userid)
    UserObject = DBSession.query(OAuthModel).filter(OAuthModel.email==userid).one()
    logging.info("found user in database")
    return UserObject
  except NoResultFound:
    pass  
  # User didn't auth normally, but maybe there's a bearer token.
  auth = request.authorization
  if 'Bearer' in auth:
      user = lookup_bearer_token(auth[1])
      UserObject = DBSession.query(OAuthModel).filter(OAuthModel.email==user['email']).one()
      headers = remember(request, UserObject.email)
      logging.info("Found user via bearer token")
      return HTTPFound("/", headers=headers)
  else:    
      return None

AccessLevels = {
   -1: "invalid",
   0: "unregistered",
   1: "g:user",
   2: "g:admin",
   255: "g:superadmin"
}

def groupfinder(userid,request):
  try:
    user = DBSession.query(OAuthModel).filter(OAuthModel.email==userid).one()
    if user is not None:
        return AccessLevels[user.AccessLevel]
  except NoResultFound:
    return None

def lookup_bearer_token(token):
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}".format(token)
    rs = requests.get(url)
    if rs.status_code == 200:
        results = rs.json()
        return results
    else:
        return None


