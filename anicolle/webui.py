#!/usr/bin/env python
import core
import json
from bottle import route, run, template, request, static_file

core.dbInit( "../bgmarker.db" )

@route("/static/<path:path>")
def home(path):
    return static_file( path, root='./public' );

@route("/")
def home():
    return template("home")

@route("/action/get/")
@route("/action/get")
def getAllBgm():
    return json.dumps( core.getAni() )

@route("/action/get/<bid>")
def getBgm( bid ):
    return json.dumps( core.getAni(int(bid)) )


run(host='localhost', port=8080, debug=1)
