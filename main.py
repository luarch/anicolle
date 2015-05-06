#!/usr/bin/env python
import sqlite3
import re
import urllib.request
import urllib.parse
import argparse
import os

aparser = argparse.ArgumentParser()
aparser.add_argument( "-a", "--add", nargs=4, metavar=("NAME","ONAIR","CUREPI", "CHKKEY"), help="Add a bgm." )
aparser.add_argument( "-rm", "--remove", type=int, metavar="ID", help="Delete a bgm." )
aparser.add_argument( "-p", "--plus", type=int, metavar="ID", help="Plus 1 to the bgm specified." )
aparser.add_argument( "-d", "--decrease", type=int, metavar="ID", help="Decrease 1 to the bgm specified." )
aparser.add_argument( "-s", "--show", type=int, metavar="ID", help="Display specified bangumi.", default=-1 )
aparser.add_argument( "-t", "--showbyday", type=int, metavar="WEEKDAY", choices=range(0,8), help="Display bangumi on specified onair day.", default=-1 )
aparser.add_argument( "-c", "--chkup", type=int, metavar="ID", help="Checkup latest updates of the specified bangumi and returns the magnet link to download" )
args = aparser.parse_args()

sqlcon = sqlite3.connect( "bgmarker.db" )
c = sqlcon.cursor();

if args.add:
    c.execute( "INSERT INTO `bangumi`( `name`, `on_air_day`, `cur_epi`, `chk_key` ) VALUES( ?, ?, ?, ? )", args.add )
    sqlcon.commit()
    print( "%s has been added as ID %d" % ( args.add[0], c.lastrowid ) )
elif args.remove:
    name = c.execute("SELECT `name`, `cur_epi` FROM `bangumi` WHERE `id` = ?", (str(args.remove),) ).fetchone()
    if name:
        name = name[0]
        print( "Are you sure to delete %s ? (Y/n)" % (name, ) )
        ec = str(input())
        if ec=='y' or ec=='Y' or ec=='':
            c.execute( "DELETE FROM `bangumi` WHERE `id` = ?", (str(args.remove), ) )
            sqlcon.commit()
            print( "ID %d has been deleted. " % args.remove )
    else:
        print("ERR: specified bgm not found.")
elif args.plus:
    name = c.execute("SELECT `name`, `cur_epi` FROM `bangumi` WHERE `id` = ?", (str(args.plus),) ).fetchone()
    if name:
        cepi = int(name[1])
        name = name[0]
        print( "Are you sure plus one to %s(%d) ? (Y/n)" % (name, cepi) )
        ec = str(input())
        if ec=='y' or ec=='Y' or ec=='':
            r = c.execute("UPDATE `bangumi` SET `cur_epi`=`cur_epi`+1 WHERE `id` = ?", (str(args.plus),) )
            sqlcon.commit()
            print( "%s has been plus one to %d" % (name, cepi+1) )
    else:
        print("ERR: specified bgm not found.")
elif args.decrease:
    name = c.execute("SELECT `name`, `cur_epi` FROM `bangumi` WHERE `id` = ?", (str(args.decrease),) ).fetchone()
    if name:
        cepi = int(name[1])
        name = name[0]
        print( "Are you sure decrease one to %s(%d) ? (Y/n)" % (name, cepi) )
        ec = str(input())
        if ec=='y' or ec=='Y' or ec=='':
            r = c.execute("UPDATE `bangumi` SET `cur_epi`=`cur_epi`-1 WHERE `id` = ?", (str(args.decrease),) )
            sqlcon.commit()
            print( "%s has been decreased one to %d" % (name, cepi-1) )
    else:
        print("ERR: specified bgm not found.")
elif args.chkup:
    name = c.execute("SELECT `name`, `chk_key`, `cur_epi` FROM `bangumi` WHERE `id` = ?", (str(args.chkup),) ).fetchone()
    if not name:
        print("ERR: specified bgm not found.")
        exit(104)
    tepi = int(name[2])+1
    chkkey = str(name[1]) + " " + "[%02d]"%tepi
    name = name[0]
    print("查找 %s 的第 %s 集资源"%( name, str(tepi) ) )
    chkkey = urllib.parse.quote_plus(chkkey)
    r = urllib.request.urlopen( "http://share.popgo.org/search.php?title=%s&sorts=1"%chkkey ).read().decode('utf-8')
    # re1 = re.compile('(magnet[^"]*)"')
    # re2 = re.compile('查看详情页[^=]*="_blank" title="([^"]*' + '%02d'%str(tepi) + '(集|话|\]|】)[^"]*)"')
    re1 = re.compile( '查看详情页.*?title="([^"]*' + '%02d'%tepi + '[集话\]】\[][^"]*)".*?(magnet[^"]*)"' )
    maglink = re.search(re1, r)
    if maglink:
        magname = maglink.group(1)
        maglink = maglink.group(2)
        print("%s\n%s"%(magname, maglink))
        if os.system('echo "%s" | xclip -in -selection clipboard'%maglink) == 0:
            print("磁力链接已拷贝到剪贴板")
    else:
        print("没有找到资源")
else:
    sqlcmd = "SELECT `id`, `name`, `cur_epi`, `on_air_day` from `bangumi`";
    if args.show>=0:
        sqlcmd += " WHERE `id` = " + str(args.show)
    if args.showbyday>=0:
        sqlcmd += " WHERE `on_air_day` = " + str(args.showbyday)
    sqlcmd += " ORDER BY `on_air_day` ASC"
    for row in c.execute( sqlcmd ):
        print( "%-3d %s\n看到%s话 每周%s更新\n" % row )
