#!/usr/bin/env python
from .. import core as core
import json
from socket import gethostname
from bottle import run, template, request, static_file, Bottle, redirect, TEMPLATE_PATH
from beaker.middleware import SessionMiddleware

app = Bottle()
workDir = "./anicolle/webui/"
TEMPLATE_PATH.append(workDir+"views")
auth_token = core.config.AUTH_TOKEN

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': False,
    'session.data_dir': './data',
    'session.auto': True
}

app_s = SessionMiddleware(app, session_opts)

def auth(callback):
    def decorator(*args, **kwargs):
        s = request.environ.get('beaker.session')
        if (not 'token' in  s) or s['token']!=auth_token:
            auth = request.get_header("X-Auth-Token")
            if auth == auth_token:
                return callback(*args, **kwargs)
            else:
                return redirect('/login')
        else:
            return callback(*args, **kwargs)
    return decorator


@app.route("/static/<path:path>")
def static(path):
    return static_file( path, root=workDir+'public' );

@app.route("/")
@auth
def home():
    return template("home", hostname = gethostname().upper() )

@app.get('/login')
def getLogin():
    return template("login", hostname = gethostname().upper())

@app.post('/login')
def postLogin():
    if(request.forms.token == auth_token) :
        s = request.environ.get('beaker.session')
        s['token'] = request.forms.token
        s.save()
        return redirect('/')
    else:
        print("[WARN] Failed to login with wrong token '", request.forms.token, "'")
        return redirect('login')

@app.get('/logout')
def getLogout():
        s = request.environ.get('beaker.session')
        s.delete()
        s.save()
        return redirect('/')

@app.route("/action/get/")
@app.route("/action/get")
@auth
def getAllBgm():
    return json.dumps( core.getAni() )

@app.route("/action/get/<bid>")
@auth
def getBgm( bid ):
    return json.dumps( core.getAni(int(bid)) )

@app.route("/action/plus/<bid>")
@auth
def plus( bid ):
    core.increase(bid)

@app.route("/action/decrease/<bid>")
@auth
def decrease( bid ):
    core.decrease(bid)

@app.post("/action/modify/<bid>")
@auth
def modify( bid ):
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    seeker = json.loads(request.forms.seeker)
    core.modify( bid, name, cur_epi, on_air, seeker )

@app.post("/action/add")
@auth
def add():
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    seeker = json.loads(request.forms.seeker)
    core.create ( name, cur_epi, on_air, seeker )

@app.route("/action/remove/<bid>")
@auth
def remove(bid):
    core.remove( bid );

@app.route("/action/chkup/<bid>")
@auth
def chkup(bid):
    return json.dumps( core.chkup(bid) );

@app.route("/action/get_seekers/")
@auth
def getSeekers():
    return json.dumps(list(core.seeker.keys()));

def start(port=core.config.SERVER_PORT):
    print("Running with ", core.run_mode, " mode.")
    port = int(port)
    run(app_s, host=core.config.SERVER_HOST, port=port, debug=core.config.DEBUG)
