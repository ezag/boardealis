from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):  # pylint:disable=unused-argument
    return {}
