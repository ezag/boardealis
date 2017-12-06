import logging

from oauthlib.common import generate_token
from oauthlib.oauth2 import MismatchingStateError
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config
from requests_oauthlib import OAuth2Session

log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):  # pylint:disable=unused-argument
    return {}


@view_config(route_name='login', renderer='templates/login.mako')
def login(request):
    settings = request.registry.settings
    request.session['oauth_state'] = generate_token()
    auth_links = []
    for provider in settings['oauth.providers'].split():
        oauth = OAuth2Session(
            settings['oauth.{}.client_id'.format(provider)],
            state=request.session['oauth_state'],
            redirect_uri=request.route_url('login_redirect', provider=provider),
            scope=settings.get('oauth.{}.scope'.format(provider)))
        url, _state = oauth.authorization_url(
            settings['oauth.{}.authorization_url'.format(provider)])
        auth_links.append((settings['oauth.{}.title'.format(provider)], url))
    return dict(auth_links=auth_links)


@view_config(route_name='login_redirect', renderer='templates/login_redirect.mako')
def login_redirect(request):
    settings = request.registry.settings
    provider = request.matchdict['provider']
    if provider not in settings['oauth.providers'].split():
        raise HTTPNotFound()
    if 'oauth_state' not in request.session:
        raise HTTPBadRequest(MismatchingStateError().description)
    oauth = OAuth2Session(
        settings['oauth.{}.client_id'.format(provider)],
        state=request.session['oauth_state'],
        redirect_uri=request.route_url('login_redirect', provider=provider))
    try:
        oauth.fetch_token(
            settings['oauth.{}.token_url'.format(provider)],
            authorization_response=request.url,
            client_secret=settings['oauth.{}.client_secret'.format(provider)])
    except MismatchingStateError as exc:
        raise HTTPBadRequest(exc.description)
    if provider == 'github':
        profile = oauth.get('https://api.github.com/user').json()
        emails = oauth.get('https://api.github.com/user/emails').json()
        result = dict(
            success=True,
            name=profile['name'],
            avatar_url=profile['avatar_url'] + '&s=256',
            email=[entry['email'] for entry in emails if entry['primary']][0],
            provider=settings['oauth.{}.title'.format(provider)],
        )
    elif provider == 'facebook':
        profile = oauth.get(
            'https://graph.facebook.com/v2.11/me?fields=id,name,email,picture').json()
        result = dict(
            success=True,
            name=profile['name'],
            avatar_url=profile['picture']['data']['url'],
            email=profile.get('email', 'NO EMAIL'),
            provider=settings['oauth.{}.title'.format(provider)],
        )
    return result
