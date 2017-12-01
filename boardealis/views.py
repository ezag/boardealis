import json

from pyramid.view import view_config
from velruse import login_url


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):  # pylint:disable=unused-argument
    return {}


@view_config(route_name='login', renderer='templates/login.mako')
def login(request):  # pylint:disable=unused-argument
    return dict(login_url=login_url)


@view_config(
    context='velruse.AuthenticationComplete',
    renderer='templates/auth_complete.mako')
def authentication_complete(request):
    context = request.context
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile': context.profile,
        'credentials': context.credentials,
    }
    return {
        'result': json.dumps(result, indent=4),
    }
