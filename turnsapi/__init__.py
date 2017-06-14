from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated, Everyone


from turnsapi.controllers.security import (groupfinder, LookupUser)

from turnsapi.models.basic import (
    DBSession,
    Base,
    )


class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'user'),
        (Allow, 'g:admin', 'admin'),
    ]

    def __init__(self, request):
        pass

def GetDB(request):
    return DBSession




def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    my_session_factory = UnencryptedCookieSessionFactoryConfig(settings['session.secret'])

    config = Configurator(settings=settings,session_factory=my_session_factory,root_factory=Root)
    authn_policy = AuthTktAuthenticationPolicy(settings['session.secret'],callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config.include('pyramid_mako')
    config.include('velruse.providers.google_oauth2')

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_google_oauth2_login_from_settings(prefix='velruse.google.')

    config.add_request_method(LookupUser,'user',reify=True)
    config.add_request_method(GetDB,'db',reify=True)

    #i18n
    config.add_subscriber('turnsapi.controllers.subscribers.add_renderer_globals', 'pyramid.events.BeforeRender')
    config.add_subscriber('turnsapi.controllers.subscribers.add_localizer', 'pyramid.events.NewRequest')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('logout','/logout')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
