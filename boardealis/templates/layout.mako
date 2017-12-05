<%inherit file="base.mako"/>
<div class="text-center">
<a href="${request.route_url('home')}">
<img class="logo img-responsive" src="${request.static_url('boardealis:static/logo14.png') }" alt="Boardealis"></img>
</a>
</div>
${next.body()}
