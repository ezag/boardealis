import json
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
        self.provider = self.request.matchdict.get('provider')

    @view_config(route_name='login', renderer='templates/login.mako')
    def login(self):
        state = generate_token()
        return dict(auth_links=[(
            self.oauth_param('title', provider),
            self.oauth_session(provider, state).authorization_url(
                self.oauth_param('authorization_url', provider))[0]
        ) for provider in self.oauth_providers])

    @view_config(route_name='login_redirect', renderer='templates/login_redirect.mako')
    def login_redirect(self):
        oauth = self.oauth_session()
        token_url = self.oauth_param('token_url')
        try:
            oauth.fetch_token(
                token_url=token_url,
                authorization_response=self.request.url,
                client_secret=self.oauth_param('client_secret'))
        except MismatchingStateError as exc:
            raise HTTPBadRequest(exc.description)
        result = getattr(self, 'profile_from_{}'.format(self.provider))(oauth)
        result.update(dict(success=True, provider=self.oauth_param('title')))
        return result

    def oauth_param(self, param, provider=None):
        provider = provider or self.provider
        assert provider is not None
        return self.request.registry.settings['oauth.{}.{}'.format(provider, param)]

    def oauth_session(self, provider=None, state=None):
        provider = provider or self.provider
        assert provider is not None
        if provider not in self.oauth_providers:
            raise HTTPNotFound()
        if state is not None:
            self.request.session['oauth_state'] = state
        elif 'oauth_state' not in self.request.session:
            raise HTTPBadRequest(MismatchingStateError().description)
        return OAuth2Session(
            client_id=self.oauth_param('client_id', provider),
            scope=self.oauth_param('scope', provider),
            redirect_uri=self.request.route_url('login_redirect', provider=provider),
            state=self.request.session['oauth_state'])

    @staticmethod
    def get_and_log(oauth, url):
        res = oauth.get(url).json()
        log.debug('GET %s %s', url, json.dumps(res, indent=2, ensure_ascii=False))
        return res

    @classmethod
    def profile_from_facebook(cls, oauth):
        profile = cls.get_and_log(
            oauth,
            'https://graph.facebook.com/v2.11/me?fields=id,name,email,picture')
        return dict(
            name=profile['name'],
            avatar_url=profile['picture']['data']['url'],
            email=profile['email'],
        )

    @classmethod
    def profile_from_github(cls, oauth):
        profile = cls.get_and_log(oauth, 'https://api.github.com/user')
        emails = cls.get_and_log(oauth, 'https://api.github.com/user/emails')
        return dict(
            name=profile['name'],
            avatar_url=profile['avatar_url'] + '&s=256',
            email=[entry['email'] for entry in emails if entry['primary']][0],
        )

    @classmethod
    def profile_from_google(cls, oauth):
        profile = cls.get_and_log(oauth, 'https://www.googleapis.com/oauth2/v3/userinfo')
        return dict(
            name=profile['name'],
            avatar_url=profile['picture'] + '?sz=256',
            email=profile['email'],
        )

    @classmethod
    def profile_from_vk(cls, oauth):  # pylint: disable=unused-argument
        return dict()
