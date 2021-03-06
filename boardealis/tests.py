import pytest
import responses


class TestsFunctional(object):
    # pylint:disable=no-self-use

    @pytest.fixture
    def app(self):
        from pyramid.paster import get_appsettings
        from webtest import TestApp
        from boardealis import main
        return TestApp(main(None, **get_appsettings('testing.ini', name='main')))

    def test_home(self, app):
        res = app.get('/', status=200)
        assert 'Добро пожаловать' in res.lxml.xpath('//title/text()')[0]
        assert '/-/login/' in res.lxml.xpath('//a/@href')

    def test_login_links(self, app):
        from urllib.parse import urlparse
        res = app.get('/-/login', status=302)
        res = app.get('/-/login/', status=200)
        assert 'Вход' in res.lxml.xpath('//title/text()')[0]
        parsed_urls = [urlparse(url) for url in res.lxml.xpath('//a/@href')]
        assert ('https', 'github.com', '/login/oauth/authorize') in [
            (url.scheme, url.hostname, url.path) for url in parsed_urls]

    def do_login_accept(self, app, provider):
        from urllib.parse import parse_qs, urlencode, urlparse
        res = app.get('/-/login/', status=200)
        state = parse_qs(urlparse(
            res.lxml.xpath('//a[text()="{}"]/@href'.format(provider))[0]
        ).query)['state'][0]
        res = app.get('/-/login/{}?{}'.format(
            provider.lower(),
            urlencode(dict(code='TEST_CODE', state=state))
        ), status=200)
        assert 'Здравствуй' in res
        assert 'Eugen Zagorodniy' in res
        assert 'eugen@example.com' in res

    @responses.activate
    def test_login_via_facebook_accept(self, app):
        responses.add(
            responses.POST, 'https://graph.facebook.com/v2.11/oauth/access_token',
            status=200, json={'access_token': 'FAKE_ACCESS_TOKEN'})
        responses.add(
            responses.GET, 'https://graph.facebook.com/v2.11/me?fields=id,name,email,picture',
            status=200, json={
                'id': '271614080033749',
                'name': 'Eugen Zagorodniy',
                'email': 'eugen@example.com',
                'picture': {
                    'data': {
                        'url': 'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/'
                               '23472236_262397077622116_7049467528256741469_n.jpg?'
                               'oh=c01240ff77a895818bc3fd80611d84ed&oe=5ACBA9B9',
                    }
                }
            })
        self.do_login_accept(app, 'Facebook')

    @responses.activate
    def test_login_via_github_accept(self, app):
        responses.add(
            responses.POST, 'https://github.com/login/oauth/access_token',
            status=200, json={'access_token': 'FAKE_ACCESS_TOKEN'})
        responses.add(
            responses.GET, 'https://api.github.com/user',
            status=200, json={
                'avatar_url': 'https://avatars0.githubusercontent.com/u/385643?v=4',
                'id': 385643,
                'name': 'Eugen Zagorodniy'})
        responses.add(
            responses.GET, 'https://api.github.com/user/emails',
            status=200, json=[{
                'email': 'eugen@example.com',
                'primary': True,
                'verified': True,
                'visibility': 'public',
            }, {
                'email': 'zagorodniy@example.com',
                'primary': False,
                'verified': True,
                'visibility': None,
            }])
        self.do_login_accept(app, 'GitHub')

    @responses.activate
    def test_login_via_google_accept(self, app):
        responses.add(
            responses.POST, 'https://www.googleapis.com/oauth2/v4/token',
            status=200, json={'access_token': 'FAKE_ACCESS_TOKEN'})
        responses.add(
            responses.GET, 'https://www.googleapis.com/oauth2/v3/userinfo',
            status=200, json={
                'sub': '102533519110366328367',
                'name': 'Eugen Zagorodniy',
                'picture': 'https://lh4.googleusercontent.com/'
                           '-Tzga_08tKs4/AAAAAAAAAAI/AAAAAAAAAHU/-NbRdil7Byc/photo.jpg',
                'email': 'eugen@example.com',
            })
        self.do_login_accept(app, 'Google')

    @pytest.mark.xfail
    # requests.exceptions.ConnectionError:
    # HTTPSConnectionPool(host='oauth.vk.com', port=443):
    # Max retries exceeded with url: /access_token
    # (Caused by NewConnectionError(
    # '<urllib3.connection.VerifiedHTTPSConnection object at 0x7f0be5f40080>:
    # Failed to establish a new connection: [Errno 111] Connection refused',))
    @responses.activate
    def test_login_via_vk_accept(self, app):
        responses.add(
            responses.POST, 'https://oauth.vk.com/access_token',
            status=200, json={'access_token': 'FAKE_ACCESS_TOKEN'})
        self.do_login_accept(app, 'VK')

    def test_login_invalid_provider(self, app):
        app.get('/-/login/invalid', status=404)

    def test_login_via_github_spoof(self, app):
        from urllib.parse import urlencode
        # Abscent state
        app.get('/-/login/github?{}'.format(urlencode(dict(
            code='TEST_CODE', state='SPOOFED_STATE'))), status=400)
        # Mismatching state
        app.get('/-/login/', status=200)
        app.get('/-/login/github?{}'.format(urlencode(dict(
            code='TEST_CODE', state='SPOOFED_STATE'))), status=400)
