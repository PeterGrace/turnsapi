from pyramid.view import view_config

from turnsapi.models.basic import DBSession
from turnsapi.models.OAuthModel import OAuthModel

from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import forbidden_view_config

from pyramid.security import remember, forget
from velruse import login_url

import logging

@forbidden_view_config(renderer='json')
def forbidden_view(request):
    if request.user is None:
        logging.info("User not yet authenticated, redirecting to google for login")
        loc=login_url(request, 'google')
        return HTTPFound(location=loc)
    else:
        return("Unauthorized")

@view_config(
  context='velruse.AuthenticationComplete',
  renderer='turnsapi:templates/AuthComplete.mak',
)
def login_complete_view(request):
  context = request.context
  result = {
    'provider_type': context.provider_type,
    'provider_name': context.provider_name,
    'profile': context.profile,
    'credentials': context.credentials,
  }
  email = context.profile['verifiedEmail']
  logging.info("User {email} has authenticated, checking their user object".format(email=email))
  try:
      MyUser = request.db.query(OAuthModel).filter(OAuthModel.email==email).one()
  except Exception:
      return HTTPForbidden()

  if hasattr(request.session,'goingto'):
    loc = request.session['goingto']
  else:
    loc = request.route_url('home', _query=(('next', request.path),))

  headers = remember(request, MyUser.email)
  return HTTPFound(location=loc, headers=headers)

@view_config(
  context='velruse.AuthenticationDenied',
  renderer='turnsapi:templates/LoginFailure.mak'
)
def login_denied_view(request):
  return { 'result': 'denied' }

@view_config(route_name='logout')
def logout_view(request):
  headers = forget(request)
  loc = request.route_url('home', _query=(('next', request.path),))
  return HTTPFound(location=loc,headers=headers)

