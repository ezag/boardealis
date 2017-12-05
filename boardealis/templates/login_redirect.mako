<%inherit file="layout.mako"/>
<%block name="title">Вход &middot; ${parent.title()}</%block>
<div class="text-center">
% if token is not None:
<p class="lead">
Входим... <code>${token}</code>
</p>
% else:
<p class="lead">
Ой, что-то пошло не так!
</p>
<p>
<a role="button" class="btn btn-lg btn-warning" href="${request.route_url('login')}">Попробовать снова</a>
</p>
% endif
</div>
