#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import core as ac
from . import webui
from .arg_parser import parse_args


def main():
    args = parse_args()
    ac.dbInit()
    if args.webui:
        webui.start()
