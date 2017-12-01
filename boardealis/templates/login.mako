<%inherit file="layout.mako"/>
<div class="text-center">
<img class="logo img-responsive" src="${request.static_url('boardealis:static/logo14.png') }" alt="Boardealis"></img>
<p class="lead">
Где у вас уже есть учётная запись? Выберите, какую использовать для входа:
</p>
<p>
<form action="${login_url(request, 'github')}" method="post">
    <input class="btn btn-lg btn-secondary" type="submit" value="GitHub" />
</form>
<form action="${login_url(request, 'facebook')}" method="post">
    <input class="btn btn-lg btn-secondary" type="submit" value="Facebook" />
</form>
</p>
