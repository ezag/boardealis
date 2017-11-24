<%inherit file="layout.mako"/>
<div class="text-center">
<img class="logo img-responsive" src="${request.static_url('boardealis:static/logo14.png') }" alt="Boardealis"></img>
<p class="lead">
<strong>Boardealis</strong><sup>*</sup> &mdash; это инструмент для тематического группового общения,
призванный совместить этику <a href="https://indieweb.org/">инди-веб</a> с удобством сервисов,
привычных большинству <del>нормальных</del> людей.
</p>
<p class="lead">
Он предназначен для того, чтобы сделать организацию путешествий, планирование выступлений,
подготовку к мероприятиям &mdash; всё то, для чего мы создаём чатики в мессенджерах, документы с
общим доступом, группы в соцсетях &mdash; легче и приятнее!
</p>
<p class="small text-right">
<sup>*</sup> <strong>board</strong> (англ. <em>доска</em>, типа объявлений) +
bor<strong>ealis</strong> (лат. <em>северное</em>, типа сияние)
<p>
<a role="button" class="btn btn-lg btn-primary btn-block" href="${request.route_path('login')}">Вход</a>
</div>

<div class="row">
<div class="col-sm-8 mx-sm-auto my-sm-5">
<h1 class="text-center">Цели и принципы</h1>

<p class="alert alert-warning">
<strong>Простите!</strong> На момент написания из нижеперечисленного не реализовано <em>ничего</em>
(кроме, разве что, открытости исходного кода); а к моменту прочтения &mdash; скорее всего <em>не
всё</em> (или <em>не так</em>). Пока проект пребывает на этапе рождения, тем не менее,
представляется существенным обозначить таким образом направление &mdash; чтобы помнить о задумке,
удерживать курс, и вновь ловить порой ускользающее вдохновление.
</p>

<h4 class="text-center">Удобство использования</h4>
<ul>
<li>Регистрация не требуется &mdash; вход через учётную запись на любом из
<a href="https://indieweb.org/silo">известных ресурсов<a>.</li>
<li>Возможность форматирования текста в наглядном, но легковесном
<a href="https://simplemde.com/">редакторе</a>.</li>
</ul>
<h4 class="text-center">Прозрачное хранение</h4>
<ul>
<li>
Информация хранится в <a href="https://indieweb.org/file-storage">текстовых файлах<a> с разметкой
<a href="https://daringfireball.net/projects/markdown/">Markdown</a> &mdash; тривиальное
импортирование, совместимость с любыми редакторами и платформами.
</li>
<li>
История изменений отслеживается посредством <a href="https://git-scm.com/">Git</a> &mdash;
проверенной и надёжной системы управления версиями.
</li>
</ul>
<h4 class="text-center">Открытая реализация</h4>
<ul>
<li>
Открытый <a href="https://github.com/ezag/boardealis">исходный код</a> &mdash; полная свобода для
желающих запустить сервис на собственном сервере, изучить реализацию или внести изменения.
</li>
<li>
Пользователи <a href="https://indieweb.org/own_your_data">владеют своими данными</a> и в любой
момент могут получить их копию в точности в том виде, в котором те хранятся на сервере &mdash; для
архивирования, резервного копирования, переноса в другую систему, собственноручной обработки, чего
угодно.
</li>
</ul>
<h1 class="text-center">Что не входит в приоритеты</h1>

<ul>
<li>
<strong>Масштабируемость.</strong> Даже если сюда придёт больше двух человек и появится больше
одного обсуждения &mdash; на улучшение производительности при увеличивающихся объёмах данных не
планируется прилагать значительно большие усилий, чем понадобились бы для введения ограничений на
количество новых пользователей и обсуждений. Предполагается, что запустить этот сервис на дешёвом
хостинге или домашнем сервере будет достаточно легко для того, чтобы в сообществе людей, которым
&laquo;не хватило места&raquo;, рано или поздно нашелся энтузиаст, желающий принять на себя такую
обязанность.<sup>**</sup>
</li>
<li>
<strong>Тонкое управление правами доступа.</strong> Кто может приглашать новых участников, кому
разрешено вносить правки, где и для кого доступно комментирование &mdash; при необходимости всё это
возможно уладить, не прибегая к техническим средствам. В чатиках, общих документах и группах в
соцсетях нас это редко заботит; избавим себя от лишних трудностей и тут.
</li>
<li>
<strong>Информационная безопасность.</strong> Разумеется, участвовать в обсуждени смогут только
приглашённые в него пользователи; каждую правку можно будет отменить; информация будет общедоступна
или скрыта в соответствии с пожеланиями её владельца; обнаруженные уязвимости будут исправляться.
Однако, особое внимание и сверхусилия на обеспечение безопасности направлены не будут &mdash; как и
чатики-домументы-группы, сервис не предназначен для данных, утечка или потеря которых катастрофична.
</li>
</ul>

<p class="small">
<sup>**</sup> Осмелюсь предположить, что Нассим Талеб одобрил бы такой подход; с доводами о благе
подобной децентрализации (в самом общем смысле, применительно к любым сферам) можно ознакомиться в
его книге &laquo;Антихрупкость. Как извлечь выгоду из хаоса&raquo;.
<p>

<h1 class="text-center">Обратная связь</h1>
<p>
Вероятнее всего, вы лично знакомы с автором проекта и отлично знаете, где и как его
найти&nbsp;<span class="lead">&#9786;</span></p>
<p>
Если же случилось невероятное и это не так, то сообщить о недостатках или пожеланиях можно в
трекере проекта на <a href="https://github.com/ezag/boardealis/issues">GitHub</a>, а по общим
вопросам связаться через <a href="https://vk.com/e.zagorodniy">VK</a> и
<a href="https://www.facebook.com/e4zag">Facebook</a>.
</p>
<p>
Этот проект в значительной мере воплощает мои ценности, предпочтения и интересы в области
информационных технологий и разработки программного обеспечения. Буду рад сотрудничеству с
единомышленниками; ознакомиться с моим резюме можно  на
<a href="https://www.linkedin.com/in/e-zag/">LinkedIn</a> и
<a href="https://www.toptal.com/resume/eugen-zagorodniy#discover-just-candid-software-developers">Toptal</a>.
<p>
</div>
</div>