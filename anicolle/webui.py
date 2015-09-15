#!/usr/bin/env python
from .  import core as core
import json
from socket import gethostname
from bottle import route, run, template, request, static_file, Bottle, TEMPLATE_PATH, auth_basic
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
@app.auth_basic(user_auth)
def home():
    return template("home", hostname = gethostname().upper() )

@app.route("/action/get/")
@app.route("/action/get")
@app.auth_basic(user_auth)
def getAllBgm():
    return json.dumps( core.getAni() )
    return 0

@app.route("/action/get/<bid>")
@app.auth_basic(user_auth)
def getBgm( bid ):
    return json.dumps( core.getAni(int(bid)) )
    return 0

@app.route("/action/plus/<bid>")
@app.auth_basic(user_auth)
def plus( bid ):
    core.plus(bid)
    pass

@app.route("/action/decrease/<bid>")
@app.auth_basic(user_auth)
def decrease( bid ):
    core.decrease(bid)
    pass

@app.post("/action/modify/<bid>")
@app.auth_basic(user_auth)
def modify( bid ):
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    chk_key = request.forms.chk_key
    core.modify( bid, name, cur_epi, on_air, chk_key )
    pass

@app.post("/action/add")
@app.auth_basic(user_auth)
def add():
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    chk_key = request.forms.chk_key
    core.add( name, cur_epi, on_air, chk_key )
    pass

@app.route("/action/remove/<bid>")
@app.auth_basic(user_auth)
def remove(bid):
    core.remove( bid );
    pass

@app.route("/action/chkup/<bid>")
@app.auth_basic(user_auth)
def chkup(bid):
    return json.dumps( core.chkup(bid) );
    return 0

def startServer(port=8080):
    port = int(port)
    run(app, host='localhost', port=port)

# if __name__ == '__main__':
#     workDir = "./"
#     TEMPLATE_PATH = workDir+"views"
#     core.dbInit( "../bgmarker.db" )
#     run(app, host='localhost', port=8080, debug=1)
