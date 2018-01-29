#!/usr/bin/env python
import argparse


def parse_args():
    aparser = argparse.ArgumentParser()
    aparser.add_argument(
        "-w", "--webui", action="store_true",
        help="Start the web-based user interface",
    )
    aparser.add_argument(
        "-v", "--version", action="store_true",
        help="Show version"
    )
    args = aparser.parse_args()
    return args
