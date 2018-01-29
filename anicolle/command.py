#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import core as ac
from . import web_api
from .arg_parser import parse_args


def main():
    args = parse_args()
    ac.dbInit()
    if args.webui:
        web_api.start()
    if args.version:
        print("Anicolle Server: v0.2.3")
