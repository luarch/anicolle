<!DOCTYPE html>
<html lang="zh-Hans">
<head>

  <!-- Basic Page Needs
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta charset="utf-8">
  <title>AniColle</title>
  <meta name="description" content="AniColle webui">
  <meta name="author" content="Chienius">

  <!-- Mobile Specific Metas
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- FONT
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <!-- <link href="http://fonts.useso.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css"> -->

  <!-- CSS
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="stylesheet" href="/static/css/normalize.css">
  <link rel="stylesheet" href="/static/css/skeleton.css">
  <link rel="stylesheet" href="/static/css/custom.css">

  <!-- Favicon
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <!-- <link rel="icon" type="image/png" href="images/favicon.png"> -->

</head>
<body>
  <div class="container">
    <div class="row action-row" style="margin-top: 10%">
      <div class="one-half column">
        <h4>AniColle</h4>
        <form action="" method="post" accept-charset="utf-8">
            <input type="password" name="token" placeholder="TOKEN">
            <input type="submit" class="button button-primary" style="width:10.0rem" value="登录"/>
        </form>
      </div>
      <div class="one-half column">
          <p style="margin-top: 2.0rem; margin-bottom: 0.5rem"><small>服务器 <b ><i>{{hostname}}</i></b></small></p>
      </div>
    </div>
  </div>
</body>
