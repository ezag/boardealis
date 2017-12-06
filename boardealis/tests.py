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

    @responses.activate
    def test_login_via_github_accept(self, app):
        from urllib.parse import parse_qs, urlencode, urlparse
        res = app.get('/-/login/', status=200)
        state = parse_qs(urlparse(
            res.lxml.xpath('//a[text()="GitHub"]/@href')[0]
        ).query)['state'][0]
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
        res = app.get('/-/login/github?{}'.format(urlencode(dict(
            code='TEST_CODE', state=state))), status=200)
        assert 'Здравствуй' in res
        assert 'Eugen Zagorodniy' in res
        assert 'eugen@example.com' in res
        assert 'zagorodniy@example.com' not in res

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
