from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound


def main(global_config, **settings):  # pylint:disable=unused-argument
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/-/login/')
    config.add_notfound_view(lambda request: HTTPNotFound(), append_slash=True)
    config.scan()
    return config.make_wsgi_app()
