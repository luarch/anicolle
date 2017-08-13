#!/usr/bin/env python
from . import core as core
import json
from bottle import run, request, response
from bottle import Bottle

app = Bottle()
workDir = "./anicolle/webui/"
auth_token = core.config.AUTH_TOKEN


def produceJson(callback):
    def decorator(*args, **kwargs):
        response.content_type = "application/json; charset=utf-8"
        return callback(*args, **kwargs)
    return decorator


def auth(callback):
    def decorator(*args, **kwargs):
        auth = request.get_header("X-Auth-Token")
        if auth == auth_token:
            return callback(*args, **kwargs)
        else:
            response.status = 401
            return "Not authorized."
    return decorator


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
            'Access-Control-Allow-Methods'
            ] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers[
            'Access-Control-Allow-Headers'
            ] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route("/get/")
@app.route("/get")
@auth
@produceJson
def getAllBgm():
    return json.dumps(core.getAni())


@app.route("/get/<bid>")
@auth
@produceJson
def getBgm(bid):
    return json.dumps(core.getAni(int(bid)))


@app.route("/plus/<bid>")
@auth
def plus(bid):
    core.increase(bid)


@app.route("/decrease/<bid>")
@auth
def decrease(bid):
    core.decrease(bid)


@app.post("/modify/<bid>")
@auth
def modify(bid):
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    seeker = json.loads(request.forms.seeker)
    core.modify(bid, name, cur_epi, on_air, seeker)


@app.post("/add")
@auth
def add():
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    seeker = json.loads(request.forms.seeker)
    core.create(name, cur_epi, on_air, seeker)


@app.route("/remove/<bid>")
@auth
def remove(bid):
    core.remove(bid)


@app.route("/chkup/<bid>")
@auth
@produceJson
def chkup(bid):
    return json.dumps(core.chkup(bid))


@app.route("/get_seekers/")
@app.route("/get_seekers")
@auth
@produceJson
def getSeekers():
    return json.dumps(list(core.seeker.keys()))


def start(port=core.config.SERVER_PORT):
    print("Running with ", core.run_mode, " mode.")
    port = int(port)
    run(app, host=core.config.SERVER_HOST,
        port=port, debug=core.config.DEBUG)
