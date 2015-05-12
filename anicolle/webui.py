#!/usr/bin/env python
import core
import json
from socket import gethostname
from bottle import route, run, template, request, static_file, Bottle

app = Bottle()

core.dbInit( "../bgmarker.db" )

@app.route("/static/<path:path>")
def home(path):
    return static_file( path, root='./public' );

@app.route("/")
def home():
    return template("home", hostname = gethostname() )

@app.route("/action/get/")
@app.route("/action/get")
def getAllBgm():
    return json.dumps( core.getAni() )

@app.route("/action/get/<bid>")
def getBgm( bid ):
    return json.dumps( core.getAni(int(bid)) )

@app.route("/action/plus/<bid>")
def plus( bid ):
    core.plus(bid)

@app.route("/action/decrease/<bid>")
def decrease( bid ):
    core.decrease(bid)

@app.post("/action/modify/<bid>")
def modify( bid ):
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    chk_key = request.forms.chk_key
    core.modify( bid, name, cur_epi, on_air, chk_key )

@app.post("/action/add")
def add():
    name = request.forms.name
    cur_epi = request.forms.cur_epi
    on_air = request.forms.on_air
    chk_key = request.forms.chk_key
    core.add( name, cur_epi, on_air, chk_key )

@app.route("/action/remove/<bid>")
def remove(bid):
    core.remove( bid );

@app.route("/action/chkup/<bid>")
def chkup(bid):
    return json.dumps( core.chkup(bid) );

run(app, host='localhost', port=8080, debug=1)
