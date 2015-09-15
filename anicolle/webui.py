#!/usr/bin/env python
from .  import core as core
import json
from socket import gethostname
from bottle import route, run, auth_basic, template, request, static_file, Bottle, TEMPLATE_PATH
from .config import config

app = Bottle()
workDir = "./anicolle/"
TEMPLATE_PATH.append(workDir+"views")
auth_user = config['default'].AUTH_USER
auth_passwd = config['default'].AUTH_PASSWD

def user_auth( user, passwd  ):
    if user == auth_user and passwd == auth_passwd:
        return True
    return False

@app.route("/static/<path:path>")
def static(path):
    return static_file( path, root=workDir+'public' );

@app.route("/")
@auth_basic(user_auth)
def home():
    return template("home", hostname = gethostname().upper() )

@app.route("/action/get/")
@app.route("/action/get")
@auth_basic(user_auth)
def getAllBgm():
    return json.dumps( core.getAni() )

@app.route("/action/get/<bid>")
@auth_basic(user_auth)
def getBgm( bid ):
    return json.dumps( core.getAni(int(bid)) )

@app.route("/action/plus/<bid>")
@auth_basic(user_auth)
def plus( bid ):
    core.plus(bid)

@app.route("/action/decrease/<bid>")
@auth_basic(user_auth)
def decrease( bid ):
    core.decrease(bid)

@app.post("/action/modify/<bid>")
@auth_basic(user_auth)
def modify( bid ):
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    chk_key = request.forms.chk_key
    core.modify( bid, name, cur_epi, on_air, chk_key )

@app.post("/action/add")
@auth_basic(user_auth)
def add():
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    chk_key = request.forms.chk_key
    core.add( name, cur_epi, on_air, chk_key )

@app.route("/action/remove/<bid>")
@auth_basic(user_auth)
def remove(bid):
    core.remove( bid );

@app.route("/action/chkup/<bid>")
@auth_basic(user_auth)
def chkup(bid):
    return json.dumps( core.chkup(bid) );

def start(port=8080):
    port = int(port)
    run(app, host='localhost', port=port)

if __name__ == '__main__':
    workDir = "./"
    TEMPLATE_PATH = workDir+"views"
    core.dbInit( "../bgmarker.db" )
    run(app, host='localhost', port=8080, debug=1)
