#!/usr/bin/env python
import core
from bottle import route, run, template, request, static_file

core.dbInit( "../bgmarker.db" )

@route("/static/<path:path>")
def home(path):
    return static_file( path, root('./public') );

@route("/")
@route("/home")
def home():
    return template("greeting", bgms=core.getAni())

@route("/action/<act>/<id:int>")
def plus(act, id):
    if not core.getAni(id):
        abort(404, "Specified bgm not found")
    if act=='plus':
        core.plus(id)
    elif act=='decrease':
        core.decrease(id)
    elif act=='chkup':
        try:
            mag = core.chkup(id)
        except:
            mag = 0
            pass
        return template("action", bgm=core.getAni(id), action=act, mag=mag)
    else:
        abort(403, "Permission denied")
    return template("action", bgm=core.getAni(id), action=act)

run(host='localhost', port=8080)
