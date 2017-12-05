import pytest


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

    def test_login(self, app):
        from urllib.parse import urlparse
        res = app.get('/-/login', status=302)
        res = app.get('/-/login/', status=200)
        assert 'Вход' in res.lxml.xpath('//title/text()')[0]
        parsed_urls = [urlparse(url) for url in res.lxml.xpath('//a/@href')]
        assert ('https', 'github.com', '/login/oauth/authorize') in [
            (url.scheme, url.hostname, url.path) for url in parsed_urls]
