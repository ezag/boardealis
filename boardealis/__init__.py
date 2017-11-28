from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):  # pylint:disable=unused-argument
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('velruse.providers.github')
    # TODO: take session secret from config
    config.set_session_factory(SignedCookieSessionFactory('itsaseekreet'))
    config.add_github_login_from_settings(prefix='velruse.github.')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/-/login/')
    config.add_notfound_view(lambda request: HTTPNotFound(), append_slash=True)
    config.scan()
    return config.make_wsgi_app()
