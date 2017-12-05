<%inherit file="layout.mako"/>
<%block name="title">Вход &middot; ${parent.title()}</%block>
<div class="text-center">
<p class="lead">
Где у вас уже есть учётная запись? Выберите, какую использовать для входа:
</p>
<p>
%for title, auth_url in auth_links:
<a role="button" class="btn btn-lg btn-secondary" href="${auth_url}">${title}</a>
%endfor
</p>
</div>
