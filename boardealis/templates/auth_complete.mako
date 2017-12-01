<%inherit file="layout.mako"/>
<div class="text-center">
<img class="logo img-responsive" src="${request.static_url('boardealis:static/logo14.png') }" alt="Boardealis"></img>
<p class="lead">
Вот что нам теперь о вас известно:
</p>
<pre class="text-left"><code>
${result}
</code></pre>
