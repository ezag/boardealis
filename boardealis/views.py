from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.mako')
def my_view(request):  # pylint:disable=unused-argument
    return {'project': 'boardealis'}
