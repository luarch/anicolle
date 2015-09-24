#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import core as ac
from . import webui
from .arg_parser import parse_args

def setSeekerData():
    r = [];
    print("设置检查器")
    while True:
        print("选择检查器类型(输入-1或回车结束): ")
        for seeker_index, seeker_name in enumerate(ac.seeker.keys()):
            print("\t", seeker_index, "\t", seeker_name)
        user_selected_seeker_idx = int(input("请选择: "))
        if user_selected_seeker_idx < 0 or not user_selected_seeker_idx:
            break
        try:
            user_selected_seeker_name = list(ac.seeker.keys())[user_selected_seeker_idx];
        except IndexError:
            print("没有找到指定的检查器，请重试")
            continue
        user_input_chk_key = input("请输入检查关键字: ")
        r_i = { 'seeker': user_selected_seeker_name, 'chk_key': user_input_chk_key }
        r.append(r_i)
    return r;

def showSeekerData(bid):
    r = ac.chkup(bid)
    if not r:
        raise LookupError
        return 0

    for item in r:
        print("[%s] %s\n%s\n" % (item['seeker'], item['title'], item['link']))
    return 1

def main():
    args = parse_args()
    ac.dbInit()

    if args.add:
        nc = ( "ID", "名称", "看到", "上映时间" )
        nc_key = ("id", "name", "cur_epi", "on_air_day")
        print( "正在添加番组" )
        n = {}
        for i in range(1, 4):
            print( "%s: " % ( nc[i], ) )
            c = str(input())
            if not c=='':
                n[nc_key[i]] = c
            else:
                if i==2 or i==3:
                    n[nc_key[i]] = 0
                else:
                    n[nc_key[i]] = ''
        n['seeker'] = setSeekerData()
        ac.create( **n )
    elif args.modify:
        nc = ( "ID", "名称", "看到", "上映时间" )
        nc_key = ("bid", "name", "cur_epi", "on_air_day")
        n = ac.getAni( args.modify )
        t = { 'bid': args.modify }
        if not n:
            print( "错误: 未找到指定番组" )
            exit()
        print( "您正在修改%s的信息" % (n['name'], ) )
        for i in range(1, 4):
            print( "%s: (回车默认 %s )" % (nc[i], str(n[nc_key[i]])) )
            c = str(input())
            if not c=='':
                t[nc_key[i]] = c
        t['seeker'] = setSeekerData()
        ac.modify( **t )
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
                ac.increase( args.plus )
                print( "%s 已加一为 %d" % (n['name'], n['cur_epi']+1 ) )
        else:
            print( "错误: 未找到指定番组" )
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
    elif args.chkup:
        # TODO Need to be reconstructured.
        if args.chkup>0:
            n = ac.getAni( args.chkup )
            if n:
                print( "查找 %s 的第 %d 集资源" % (n['name'], n['cur_epi']+1) )
                try:
                    showSeekerData(n['id'])
                except NameError:
                    print( "ERR: specified bgm not found." )
                except LookupError:
                    print( "没有找到相关资源" )
        elif args.chkup==-1:
            print( "查找所有资源" )
            n = ac.getAni()
            i = 0
            for row in n:
                try:
                    if showSeekerData(n['id']):
                        i = i+1
                except:
                    continue
                    pass
            else:
                print( "%d个资源有更新" % i )
    elif args.webui:
        webui.start();
        pass
    else:
        r = ac.getAni( args.show, args.showbyday )
        if args.show>=0:
            print( "%-3d %s\t已看%s/周%s更新" % (r['id'], r['name'], r['cur_epi'], str(r['on_air_day'])) )
        else:
            for row in r:
                print( "%-3d %s\t已看%s/周%s更新" % (row['id'], row['name'], row['cur_epi'], str(row['on_air_day']) ))
