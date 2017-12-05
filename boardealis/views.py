from pyramid.view import view_config
from requests_oauthlib import OAuth2Session


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):  # pylint:disable=unused-argument
    return {}


@view_config(route_name='login', renderer='templates/login.mako')
def login(request):  # pylint:disable=unused-argument
    settings = request.registry.settings
    oauth = OAuth2Session(
        settings['oauth.github.client_id'],
        redirect_uri=request.route_url('login'),
        scope=settings['oauth.github.scope'])
    url, state = oauth.authorization_url(settings['oauth.github.authorization_url'])
    return dict(github_url=url)
