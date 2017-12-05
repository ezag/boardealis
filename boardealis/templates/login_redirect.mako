<%inherit file="layout.mako"/>
<%block name="title">Вход &middot; ${parent.title()}</%block>
<div class="text-center">
% if success:
<p class="lead">
Здравствуй, <strong>${name}</strong>!
</p>
<div>
<img class="img-responsive" src="${avatar_url}" alt="${name}"></img>
</div>
<div class="alert alert-warning text-left col-sm-8 mx-sm-auto my-sm-5">
<p>
Пока что тут будут обращаться к тебе так, как ${provider} тебя и представил:
<strong>${name}</strong>. <em>Когда-нибудь</em> появится возможность указать
своё имя так, как тебе нравится.
</p>
<p>
А ещё <em>когда-нибудь</em> по адресу электронной почты <code>${email}</code>
мы сможем узнать тебя, если ты зайдёшь, использовав другую учётную запись. Пока
что же просим заходить через ${provider} &mdash; иначе мы примем тебя за нового
человека, и ты окажешься без доступа ко всему тому, к чему он у тебя должен
быть.
</p>
<p>
Эти неудобства &mdash; цена как можно более раннего запуска минимально рабочей
версии сервиса. Надеемся на понимание!
</p>
</div>
<p>
<a role="button" class="btn btn-lg btn-success btn-block" href="#">Хорошо</a>
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
