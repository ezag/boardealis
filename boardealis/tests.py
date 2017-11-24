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
        assert b'Boardealis' in res.body
