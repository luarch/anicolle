#!/usr/bin/env python
"""AniColle Library

Collect your animes like a geek.
"""

import sqlite3 as _sqlite3
import re as _re
import urllib.request as _ur
import urllib.parse as _up

def dbInit( dbname="bgmarker.db" ):
    global sqlcon, sqlcur
    sqlcon = _sqlite3.connect( dbname )
    sqlcur = sqlcon.cursor()
    sqlcur.execute("CREATE TABLE IF NOT EXISTS bangumi ( id INTEGER PRIMARY KEY AUTOINCREMENT, name, cur_epi INTEGER DEFAULT 0, on_air_epi INTEGER DEFAULT 0, on_air_day INTEGER DEFAULT 0 , `chk_key` DEFAULT '');")

def getAni( bid=-1, on_air_day=-1 ):
    sqlcmd = "SELECT `id`, `name`, `cur_epi`, `on_air_day`, `chk_key` from `bangumi`";
    if bid>=0:
        sqlcmd += " WHERE `id` = " + str(bid)
    if on_air_day>=0:
        sqlcmd += " WHERE `on_air_day` = " + str(on_air_day)
    sqlcmd += " ORDER BY `on_air_day` ASC"
    r = []
    for row in sqlcur.execute( sqlcmd ).fetchall():
        r.append(list(row))
    if bid>=0 and r:
        r = r[0]
    return r

def add( name, cur_epi=0, on_air_day=0, chk_key="" ):
    sqlcur.execute(
        "INSERT INTO `bangumi`( `name`, `on_air_day`, `cur_epi`, `chk_key` ) VALUES( ?, ?, ?, ? )",
        ( name, int(on_air_day), int(cur_epi), chk_key )
    )
    sqlcon.commit()

def modify( bid, name, cur_epi=0, on_air_day=0, chk_key="" ):
    sqlcur.execute( "UPDATE `bangumi` SET `name` = ? WHERE `id` = ?", ( name, bid ) )
    sqlcur.execute( "UPDATE `bangumi` SET `cur_epi` = ? WHERE `id` = ?", ( int(cur_epi), bid ) )
    sqlcur.execute( "UPDATE `bangumi` SET `on_air_day` = ? WHERE `id` = ?", ( int(on_air_day), bid ) )
    sqlcur.execute( "UPDATE `bangumi` SET `chk_key` = ? WHERE `id` = ?", ( chk_key, bid ) )
    sqlcon.commit()

def remove(bid):
    sqlcur.execute( "DELETE FROM `bangumi` WHERE `id` = ?", (str(bid), ) )
    sqlcon.commit()

def plus( bid ):
    sqlcur.execute("UPDATE `bangumi` SET `cur_epi`=`cur_epi`+1 WHERE `id` = ?", (str(bid),) )
    sqlcon.commit()

def decrease( bid ):
    sqlcur.execute("UPDATE `bangumi` SET `cur_epi`=`cur_epi`-1 WHERE `id` = ?", (str(bid),) )
    sqlcon.commit()

def chkup( bid ):
    name = sqlcur.execute("SELECT `name`, `chk_key`, `cur_epi`, `on_air_day` FROM `bangumi` WHERE `id` = ?", (str(bid),) ).fetchone()
    if not name[1] or not name[3]:
        return 0
    tepi = int(name[2])+1
    chkkey = str(name[1]) + " " + "[%02d] MP4"%tepi
    name = name[0]
    chkkey = _up.quote_plus(chkkey)
    r = _ur.urlopen( "http://share.popgo.org/search.php?title=%s&sorts=1"%chkkey ).read().decode('utf-8')
    re1 = _re.compile( '查看详情页.*?title="([^"]*' + '%02d'%tepi + '[集话\]】\[][^"]*)".*?(magnet[^"]*)"' )
    maglink = _re.search(re1, r)
    if maglink:
        magname = maglink.group(1)
        maglink = maglink.group(2)
        return { "magname": magname, "maglink": maglink }
    else:
        return 0
