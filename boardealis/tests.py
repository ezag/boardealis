import pytest


class TestsFunctional(object):
    # pylint:disable=no-self-use

    @pytest.fixture
    def app(self):
        from boardealis import main
        from webtest import TestApp
        return TestApp(main({}))

    def test_home(self, app):
        res = app.get('/', status=200)
        assert 'Добро пожаловать' in res.lxml.xpath('//title/text()')[0]
        assert '/-/login/' in res.lxml.xpath('//a/@href')

    @pytest.mark.xfail
    def test_login(self, app):
        res = app.get('/-/login', status=302)
        res = app.get('/-/login/', status=200)
        assert 'Вход' in res.lxml.xpath('//title/text()')[0]
