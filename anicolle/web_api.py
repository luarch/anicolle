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
    def returnEmpty():
        return None

    def decorator(*args, **kwargs):
        auth = request.get_header("X-Auth-Token")
        if request.method == 'OPTIONS':
            return returnEmpty()
        elif auth == auth_token:
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
            ] = 'Origin, Accept, Content-Type, X-Requested-With, X-Auth-Token'


@app.route("/checkpoint", method=['GET', 'OPTIONS'])
@auth
@produceJson
def checkPoint():
    return {'status': 'success'}


@app.route("/get/", method=['GET', 'OPTIONS'])
@app.route("/get", method=['GET', 'OPTIONS'])
@auth
@produceJson
def getAllBgm():
    search = request.query.search
    bgms = core.getAni()
    r = []
    for bgm in bgms:
        if search in bgm['name'] or search in bgm['name_pinyin']:
            r.append(bgm)
    return json.dumps(r)


@app.route("/get/<bid>", method=['GET', 'OPTIONS'])
@auth
@produceJson
def getBgm(bid):
    return json.dumps(core.getAni(int(bid)))


@app.route("/plus/<bid>", method=['GET', 'OPTIONS'])
@auth
@produceJson
def plus(bid):
    return json.dumps(core.increase(bid))


@app.route("/decrease/<bid>", method=['GET', 'OPTIONS'])
@auth
@produceJson
def decrease(bid):
    return json.dumps(core.decrease(bid))


@app.route("/modify/<bid>", method=['POST', 'OPTIONS'])
@auth
@produceJson
def modify(bid):
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    if request.forms.seeker:
        seeker = json.loads(request.forms.seeker)
    else:
        seeker = None
    bgm_dict = core.modify(bid, name, cur_epi, on_air, seeker)
    return json.dumps(bgm_dict)


@app.route("/add", method=['POST', 'OPTIONS'])
@auth
@produceJson
def add():
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    seeker = json.loads(request.forms.seeker)
    bgm_dict = core.create(name, cur_epi, on_air, seeker)
    return json.dumps(bgm_dict)


@app.route("/remove/<bid>", method=['GET', 'OPTIONS'])
@auth
def remove(bid):
    core.remove(bid)


@app.route("/chkup/<bid>", method=['GET', 'OPTIONS'])
@auth
@produceJson
def chkup(bid):
    episode = request.query.episode
    return json.dumps(core.chkup(bid, episode))


@app.route("/get_seekers/", method=['GET', 'OPTIONS'])
@app.route("/get_seekers", method=['GET', 'OPTIONS'])
@auth
@produceJson
def getSeekers():
    return json.dumps(list(core.seeker.keys()))


def start(port=core.config.SERVER_PORT):
    print("Running with ", core.run_mode, " mode.")
    port = int(port)
    run(app, host=core.config.SERVER_HOST,
        port=port, debug=core.config.DEBUG)
