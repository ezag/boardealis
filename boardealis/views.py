from pyramid.view import view_config
from velruse import login_url


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):  # pylint:disable=unused-argument
    return {}


@view_config(route_name='login', renderer='templates/login.mako')
def login(request):  # pylint:disable=unused-argument
    return dict(login_url=login_url)
