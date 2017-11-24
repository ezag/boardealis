import unittest

from pyramid import testing


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from boardealis import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        assert b'Boardealis' in res.body
