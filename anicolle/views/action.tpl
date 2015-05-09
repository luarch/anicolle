<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AniColle</title>
</head>
<body>
    <p>已完成 {{bgm[1]}} ({{bgm[2]}}) {{action}}</p>
% if action == 'chkup':
%   if mag:
    <p>{{mag['maglink']}}<br>{{mag['magname']}}</p>
%   else:
    <p>未发现更新</p>
%   end
% end
    <a href="/">返回</a>
</body>
</html>
