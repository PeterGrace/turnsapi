<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alchemy Scaffold for The Pyramid Web Framework</title>

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_url('turnsapi:static/css/bootstrap.min.css')}" rel="stylesheet">
    <link href="${request.static_url('turnsapi:static/css/bootstrap-theme.css')}" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="//oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
<script type="text/javascript">
    function addLoadEvent(func) {
        var oldonload = window.onload;
        if (typeof window.onload != 'function') {
            window.onload = func;
        } else {
            window.onload = function() {
                if (oldonload) {
                    oldonload();
                }
                func();
            }
        }
    }

    //http://stackoverflow.com/a/13371349/274549
    var escapeHtml = (function () {
        'use strict';
        var chr = { '"': '&quot;', '&': '&amp;', '<': '&lt;', '>': '&gt;' };
        return function (text) {
            return text.replace(/[\"&<>]/g, function (a) { return chr[a]; });
        };
    }());
</script>
<nav class="navbar navbar-inverse navbar-static-top">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">${_(u"Toggle navigation")}</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <span class="navbar-brand">${_(u"turnsapi")}</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
                <li><a href="/">Home</a></li>
            </ul>
<%
  from velruse import login_url
  from pyramid.httpexceptions import HTTPFound
  logged_in=request.user()
  if isinstance(logged_in, HTTPFound):
      return logged_in
  loginurl=login_url(request, 'google')
  logouturl=request.route_url('logout')
%>

<p class="navbar-btn navbar-right">
% if logged_in is not None:
            <a class="btn btn-default" href="${logouturl}">${_(u"{email} - Logout", logged_in.email)}</a>
% else:
            <a class="btn btn-default" href="${loginurl}">${_(u"Login")}</a>
% endif
</p>


        </div><!--/.nav-collapse -->
    </div>
</nav>
<div class="alert-messages text-center">
</div>


<div class="container">
<%block name="BlockContent"/>
</div> <!-- container -->

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="${request.static_url('turnsapi:static/js/bootstrap.min.js')}"></script>
<script src="${request.static_url('turnsapi:static/js/bootstrap-modal.js')}"></script>

<script>
function showAndDismissAlert(type, message) {
    var htmlAlert = '<div class="alert alert-' + type + '">' + message + '</div>';

    // Prepend so that alert is on top, could also append if we want new alerts to show below instead of on top.
    $(".alert-messages").prepend(htmlAlert);

    // Since we are prepending, take the first alert and tell it to fade in and then fade out.
    // Note: if we were appending, then should use last() instead of first()
    $(".alert-messages .alert").first().hide().fadeIn(200).delay(2000).fadeOut(1000, function () { $(this).remove(); });
}
</script>

<%block name="ScriptContent"/>

      

  </body>
</html>
