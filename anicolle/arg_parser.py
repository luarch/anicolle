#!/usr/bin/env python
import argparse


def parse_args():
    aparser = argparse.ArgumentParser()
    aparser.add_argument(
        "-w", "--webui", action="store_true",
        help="Start the web-based user interface"
    )
    args = aparser.parse_args()
    return args
