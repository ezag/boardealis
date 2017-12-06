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


class LoginViews(object):
    def __init__(self, request):
        self.request = request
        self.oauth_providers = request.registry.settings['oauth.providers'].split()

    @view_config(route_name='login', renderer='templates/login.mako')
    def login(self):
        state = generate_token()
        return dict(auth_links=[(
            self.oauth_param(provider, 'title'),
            self.oauth_session(provider, state).authorization_url(
                self.oauth_param(provider, 'authorization_url'))[0]
        ) for provider in self.oauth_providers])

    @view_config(route_name='login_redirect', renderer='templates/login_redirect.mako')
    def login_redirect(self):
        provider = self.request.matchdict['provider']
        oauth = self.oauth_session(provider)
        try:
            oauth.fetch_token(
                token_url=self.oauth_param(provider, 'token_url'),
                authorization_response=self.request.url,
                client_secret=self.oauth_param(provider, 'client_secret'))
        except MismatchingStateError as exc:
            raise HTTPBadRequest(exc.description)
        result = getattr(self, 'profile_from_{}'.format(provider))(oauth)
        result.update(dict(success=True, provider=self.oauth_param(provider, 'title')))
        return result

    def oauth_param(self, provider, param):
        return self.request.registry.settings['oauth.{}.{}'.format(provider, param)]

    def oauth_session(self, provider, state=None):
        if provider not in self.oauth_providers:
            raise HTTPNotFound()
        if state is not None:
            self.request.session['oauth_state'] = state
        elif 'oauth_state' not in self.request.session:
            raise HTTPBadRequest(MismatchingStateError().description)
        return OAuth2Session(
            client_id=self.oauth_param(provider, 'client_id'),
            scope=self.oauth_param(provider, 'scope'),
            redirect_uri=self.request.route_url('login_redirect', provider=provider),
            state=self.request.session['oauth_state'])

    @staticmethod
    def profile_from_facebook(oauth):
        profile = oauth.get(
            'https://graph.facebook.com/v2.11/me?fields=id,name,email,picture').json()
        return dict(
            name=profile['name'],
            avatar_url=profile['picture']['data']['url'],
            email=profile['email'],
        )

    @staticmethod
    def profile_from_github(oauth):
        profile = oauth.get('https://api.github.com/user').json()
        emails = oauth.get('https://api.github.com/user/emails').json()
        return dict(
            name=profile['name'],
            avatar_url=profile['avatar_url'] + '&s=256',
            email=[entry['email'] for entry in emails if entry['primary']][0],
        )
