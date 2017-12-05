<%inherit file="layout.mako"/>
<%block name="title">Вход &middot; ${parent.title()}</%block>
<div class="text-center">
<p class="lead">
Где у вас уже есть учётная запись? Выберите, какую использовать для входа:
</p>
<p>
<a role="button" class="btn btn-lg btn-secondary" href="#">Google</a>
<a role="button" class="btn btn-lg btn-secondary" href="#">Twitter</a>
<a role="button" class="btn btn-lg btn-secondary" href="#">Facebook</a>
<a role="button" class="btn btn-lg btn-secondary" href="#">VK</a>
<a role="button" class="btn btn-lg btn-secondary" href="${github_url}">GitHub</a>
</p>
</div>
