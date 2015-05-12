#!/usr/bin/env python
import argparse
import anicolle.core as anicolle
import os

anicolle.dbInit()

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
args = aparser.parse_args()



if args.add:
    nc = ( "ID", "名称", "看到", "上映时间", "检查关键字" )
    print( "正在添加番组" )
    n = [0, 0, 0, 0, 0]
    for i in range(1, 5):
        print( "%s: " % ( nc[i], ) )
        c = str(input())
        if not c=='':
            n[i] = c
        else:
            if i==2 or i==3:
                n[i] = 0
            else:
                n[i] = ''
    anicolle.add( n[1], n[2], n[3], n[4] )
elif args.modify:
    nc = ( "ID", "名称", "看到", "上映时间", "检查关键字" )
    n = anicolle.getAni( args.modify )
    t = list(n)
    if not n:
        print( "错误: 未找到指定番组" )
        exit()
    print( "您正在修改%s的信息" % (n[1], ) )
    for i in range(1, 5):
        print( "%s: (回车默认 %s )" % (nc[i], str(n[i])) )
        c = str(input())
        if not c=='':
            t[i] = c
    anicolle.modify( args.modify, t[1], t[2], t[3], t[4] )
elif args.remove:
    n = anicolle.getAni( args.remove )
    if n:
        n = n[1:2]
        n = tuple(n)
        print( "确定删除%s吗？(Y/n)" % n )
        c = str(input())
        if c=='' or c=='Y' or c=='y':
            anicolle.remove( args.remove )
            print( "%s 已删除" % n  )
    else:
        print( "错误: 未找到指定番组" )
elif args.plus:
    n = anicolle.getAni( args.plus )
    if n:
        n = n[1:3]
        n = tuple(n)
        print( "确定向%s(%d)加一吗？(Y/n)" % n )
        c = str(input())
        if c=='' or c=='Y' or c=='y':
            anicolle.plus( args.plus )
            print( "%s 已加一为 %d" % ( n[0], n[1]+1 ) )
    else:
        print( "错误: 未找到指定番组" )
elif args.decrease:
    n = anicolle.getAni( args.decrease )
    if n:
        n = n[1:3]
        n = tuple(n)
        print( "确定向%s(%d)减一吗？(Y/n)" % n )
        c = str(input())
        if c=='' or c=='Y' or c=='y':
            anicolle.decrease( args.decrease )
            print( "%s 已减一为 %d" % ( n[0], n[1]-1 ) )
    else:
        print( "错误: 未找到指定番组" )
elif args.chkup:
    if args.chkup>0:
        n = anicolle.getAni( args.chkup )
        if n:
            print( "查找 %s 的第 %d 集资源" % (n[1], n[2]+1) )
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
                if r:
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
    if args.show>=0:
        r = r[0:4]
        r = tuple(r)
        print( "%-3d %s\t已看%s/周%s更新" % r )
    else:
        for row in r:
            row = row[0:4]
            row = tuple(row)
            print( "%-3d %s\t已看%s/周%s更新" % row )
