#!/usr/bin/env python
import argparse

def parse_args():
    aparser = argparse.ArgumentParser()
    aparser.add_argument(
        "-a", "--add", nargs="?", const="1"
    )
    aparser.add_argument(
        "-m", "--modify", type=int,
        metavar="ID", help="Modify a bgm."
    )
    aparser.add_argument(
        "-rm", "--remove", type=int,
        metavar="ID", help="Delete a bgm."
    )
    aparser.add_argument(
        "-p", "--plus", type=int,
        metavar="ID", help="Plus 1 to the bgm specified."
    )
    aparser.add_argument(
        "-d", "--decrease", type=int,
        metavar="ID", help="Decrease 1 to the bgm specified."
    )
    aparser.add_argument(
        "-s", "--show", type=int,
        metavar="ID", help="Display specified bangumi.", default=-1
    )
    aparser.add_argument(
        "-t", "--showbyday", type=int,
        metavar="WEEKDAY", choices=range(0,8),
        help="Display bangumi on specified onair day.", default=-1
    )
    aparser.add_argument(
        "-c", "--chkup", type=int,
        metavar="ID",
        help="Checkup latest updates of the specified bangumi and returns the magnet link to download",
        const=-1, nargs='?'
    )
    aparser.add_argument(
        "-w", "--webui", action="store_true",
        help="Start the web-based user interface"
    )
    args = aparser.parse_args()
    return args

