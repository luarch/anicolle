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

  <!-- Scripts
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <script src="/static/lib/jquery.min.js"></script>
  <script src="/static/lib/global.js"></script>

</head>
<body>

  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <div class="container">
    <div class="row action-row" style="margin-top: 10%">
      <div class="one-half column">
        <h4>AniColle</h4>
        <input type="text" placeholder="搜索...">
      </div>
      <div class="one-half column">
          <p style="margin-top: 2.0rem; margin-bottom: 0.5rem"><small>服务器 <b ><i>{{hostname}}</i></b></small></p>
          <a href="#" class="button button-primary" style="width:20.4rem">检查全部</a>
          <br>
          <a href="admin" class="button" style="width:10.0rem">管理</a>
          <a href="admin" class="button" style="width:10.0rem">退出</a>
      </div>
    </div>

    <div class="row bgm-row" style="margin-top: 50px" data-bid="0">
        <div class="two-thirds column">
            <h3>
                <a href="javascript:void(0)">正在加载...</a>
            </h3>
        </div>
    </div>

    <div class="row plus-row" style="margin-top: 50px">
        <div class="two-thirds column">
            <h3><a href="javascript:void(0)" class="bgm-title">[ + ]</a></h3>
        </div>
    </div>

    <div class="row" style="font-size: small; text-align: right; color: #555;">
        <p>Presented by Chienius with &hearts;.</p>
    </div>

  </div>

<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
</html>
