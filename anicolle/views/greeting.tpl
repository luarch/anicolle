<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AniColle</title>
</head>
<body>
    <table>
        <tr>
            <th>ID</th>
            <th>名称</th>
            <th>看到</th>
            <th>更新于</th>
            <th>操作</th>
        </tr>
        % for bgm in bgms:
        <tr>
            <td>{{bgm[0]}}</td>
            <td>{{bgm[1]}}</td>
            <td>{{bgm[2]}}</td>
            <td>{{bgm[3]}}</td>
            <td>
                <a href="action/plus/{{bgm[0]}}">+1</a>
                <a href="action/decrease/{{bgm[0]}}">-1</a>
                <a href="action/chkup/{{bgm[0]}}">查新</a>
            </td>
        </tr>
        % end
    </table>
</body>
</html>
