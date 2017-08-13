#!/usr/bin/env python
from .. import core as core
import json
from bottle import run, request
from bottle import Bottle

app = Bottle()
workDir = "./anicolle/webui/"
auth_token = core.config.AUTH_TOKEN


def auth(callback):
    def decorator(*args, **kwargs):
        auth = request.get_header("X-Auth-Token")
        if auth == auth_token:
            return callback(*args, **kwargs)
        else:
            return 401
    return decorator


@app.route("/action/get/")
@app.route("/action/get")
@auth
def getAllBgm():
    return json.dumps(core.getAni())


@app.route("/action/get/<bid>")
@auth
def getBgm(bid):
    return json.dumps(core.getAni(int(bid)))


@app.route("/action/plus/<bid>")
@auth
def plus(bid):
    core.increase(bid)


@app.route("/action/decrease/<bid>")
@auth
def decrease(bid):
    core.decrease(bid)


@app.post("/action/modify/<bid>")
@auth
def modify(bid):
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    seeker = json.loads(request.forms.seeker)
    core.modify(bid, name, cur_epi, on_air, seeker)


@app.post("/action/add")
@auth
def add():
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    seeker = json.loads(request.forms.seeker)
    core.create(name, cur_epi, on_air, seeker)


@app.route("/action/remove/<bid>")
@auth
def remove(bid):
    core.remove(bid)


@app.route("/action/chkup/<bid>")
@auth
def chkup(bid):
    return json.dumps(core.chkup(bid))


@app.route("/action/get_seekers/")
@auth
def getSeekers():
    return json.dumps(list(core.seeker.keys()))


def start(port=core.config.SERVER_PORT):
    print("Running with ", core.run_mode, " mode.")
    port = int(port)
    run(app, host=core.config.SERVER_HOST,
        port=port, debug=core.config.DEBUG)
