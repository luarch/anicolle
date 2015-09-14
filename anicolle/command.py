#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import core as ac
import os
from .arg_parser import parse_args

def main():
    args = parse_args()

    if args.add:
        # nc = ( "ID", "名称", "看到", "上映时间", "检查关键字" )
        # print( "正在添加番组" )
        # n = [0, 0, 0, 0, 0]
        # for i in range(1, 5):
            # print( "%s: " % ( nc[i], ) )
            # c = str(input())
            # if not c=='':
                # n[i] = c
            # else:
                # if i==2 or i==3:
                    # n[i] = 0
                # else:
                    # n[i] = ''
        # ac.add( n[1], n[2], n[3], n[4] )
        pass
    elif args.modify:
        # nc = ( "ID", "名称", "看到", "上映时间", "检查关键字" )
        # n = ac.getAni( args.modify )
        # t = list(n)
        # if not n:
            # print( "错误: 未找到指定番组" )
            # exit()
        # print( "您正在修改%s的信息" % (n[1], ) )
        # for i in range(1, 5):
            # print( "%s: (回车默认 %s )" % (nc[i], str(n[i])) )
            # c = str(input())
            # if not c=='':
                # t[i] = c
        # ac.modify( args.modify, t[1], t[2], t[3], t[4] )
        pass
    elif args.remove:
        n = ac.getAni( args.remove )
        if n:
            print( "确定删除%s吗？(Y/n)" % (n['name'],  ) )
            c = str(input())
            if c=='' or c=='Y' or c=='y':
                ac.remove( args.remove )
                print( "%s 已删除" % n['name']  )
        else:
            print( "错误: 未找到指定番组" )
    elif args.plus:
        n = ac.getAni( args.plus )
        if n:
            print( "确定向%s(%d)加一吗？(Y/n)" % (n['name'], n['cur_epi'] ) )
            c = str(input())
            if c=='' or c=='Y' or c=='y':
                ac.plus( args.plus )
                print( "%s 已加一为 %d" % (n['name'], n['cur_epi']+1 ) )
        else:
            print( "错误: 未找到指定番组" )
        pass
    elif args.decrease:
        n = ac.getAni( args.decrease )
        if n:
            print( "确定向%s(%d)减一吗？(Y/n)" % (n['name'], n['cur_epi'] ) )
            c = str(input())
            if c=='' or c=='Y' or c=='y':
                ac.decrease( args.decrease )
                print( "%s 已减一为 %d" % (n['name'], n['cur_epi']-1 ) )
        else:
            print( "错误: 未找到指定番组" )
        pass
    elif args.chkup:
        if args.chkup>0:
            n = ac.getAni( args.chkup )
            if n:
                print( "查找 %s 的第 %d 集资源" % (n['name'], n['cur_epi']+1) )
                try:
                    r = ac.chkup(args.chkup)
                    print("%s\n%s"%(r['magname'], r['maglink']))
                    if os.system('echo "%s" | xclip -in -selection clipboard'%r['maglink']) == 0:
                        print("磁力链接已拷贝到剪贴板")
                except NameError:
                    print( "ERR: specified bgm not found." )
                except LookupError:
                    print( "没有找到相关资源" )
        elif args.chkup==-1:
            print( "查找所有资源" )
            n = ac.getAni()
            i = 0
            mls = []
            for row in n:
                try:
                    r = ac.chkup(row['id'])
                except:
                    continue
                    pass
                else:
                    if r:
                        print( "%-3d %s\n有更新: %s\n" % (row['id'], row['name'], r['magname']) )
                        mls.append(r['maglink'])
                        i = i+1
            if not i:
                print( "没有找到有更新的资源" )
            else:
                print( "%d个资源有更新" % i )
                if os.system('echo -e "%s" | xclip -in -selection clipboard'%( '\n'.join(mls), )) == 0:
                    print("磁力链接已拷贝到剪贴板")
        pass
    elif args.webui:
        # webui.start(args.webui);
        pass
    else:
        r = ac.getAni( args.show, args.showbyday )
        if args.show>=0:
            print( "%-3d %s\t已看%s/周%s更新" % (r['id'], r['name'], r['cur_epi'], str(r['on_air_day'])) )
        else:
            for row in r:
                print( "%-3d %s\t已看%s/周%s更新" % (row['id'], row['name'], row['cur_epi'], str(row['on_air_day']) ))
        pass
