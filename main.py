#!/usr/bin/env python
import argparse
import anicolle
import os

anicolle.dbInit()

aparser = argparse.ArgumentParser()
aparser.add_argument(
    "-a", "--add", nargs=4,
    metavar=("NAME","ONAIR","CUREPI", "CHKKEY"), help="Add a bgm."
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
args = aparser.parse_args()



if args.add:
    anicolle.add( args.add[0], args.add[1], args.add[2], args.add[3] )
elif args.plus:
    anicolle.plus( args.plus )
elif args.decrease:
    anicolle.decrease( args.decrease )
elif args.chkup:
    if args.chkup>0:
        n = anicolle.getAni( args.chkup )
        if n:
            print( "查找 %s 的第 %d 集资源" % (n[0][1], n[0][2]+1) )
            try:
                r = anicolle.chkup(args.chkup)
                print("%s\n%s"%(r['magname'], r['maglink']))
                if os.system('echo "%s" | xclip -in -selection clipboard'%r['maglink']) == 0:
                    print("磁力链接已拷贝到剪贴板")
            except NameError:
                print( "ERR: specified bgm not found." )
            except LookupError:
                print( "没有找到相关资源" )
    elif args.chkup==-1:
        print( "查找所有资源" )
        n = anicolle.getAni()
        i = 0
        mls = []
        for row in n:
            try:
                r = anicolle.chkup(row[0])
            except:
                continue
                pass
            else:
                print( "%-3d %s\n有更新: %s\n" % (row[0], row[1], r['magname']) )
                mls.append(r['maglink'])
                i = i+1
        if not i:
            print( "没有找到有更新的资源" )
        else:
            print( "%d个资源有更新" % i )
            if os.system('echo -e "%s" | xclip -in -selection clipboard'%( '\n'.join(mls), )) == 0:
                print("磁力链接已拷贝到剪贴板")
else:
    r = anicolle.getAni( args.show, args.showbyday )
    for row in r:
        print( "%-3d %s\t已看%s/周%s更新" % row )
