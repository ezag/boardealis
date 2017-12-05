from pyramid.view import view_config
from requests_oauthlib import OAuth2Session


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):  # pylint:disable=unused-argument
    return {}


@view_config(route_name='login', renderer='templates/login.mako')
def login(request):  # pylint:disable=unused-argument
    settings = request.registry.settings
    auth_links = []
    for provider in settings['oauth.providers'].split():
        oauth = OAuth2Session(
            settings['oauth.{}.client_id'.format(provider)],
            redirect_uri=request.route_url('login'),
            scope=settings['oauth.{}.scope'.format(provider)])
        url, state = oauth.authorization_url(
            settings['oauth.{}.authorization_url'.format(provider)])
        auth_links.append((settings['oauth.{}.title'.format(provider)], url))
    return dict(auth_links=auth_links)
