#!/usr/bin/env python
"""AniColle Library

Collect your animes like a geek.

Database model and operations here.
Unlike the previous version, this version returns objects as results rather than dictionaries in previous version.
You can force convert it into a dict by using to_dict().
"""

from peewee import *
from .config import config
import re as _re
import urllib.request as _ur
import urllib.parse as _up

db = SqliteDatabase(config['default'].DATABASE)

class Bangumi(Model):
    # `id` field is added automatically
    name = TextField()
    cur_epi = IntegerField(default=0)
    on_air_epi = IntegerField(default=0)
    on_air_day = IntegerField(default=0)
    chk_key = TextField(default='')
    class Meta:
        database = db

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cur_epi': self.cur_epi,
            'on_air_epi': self.on_air_epi,
            'on_air_epi': self.on_air_day,
            'chk_key': self.chk_key
        }

def dbInit():
    db.connect()
    db.create_tables([Bangumi], safe=True)
    db.close()

def getAni( bid=-1, on_air_day=-1 ):
    db.connect()
    r = []
    try:
        if bid>=0:
            # get a single record
            r = Bangumi.get(Bangumi.id==bid)
        elif on_air_day>=0:
            # get a set of records
            for bgm in Bangumi.select().where(Bangumi.on_air_day==on_air_day):
                r.append(bgm)
        else:
            # get all records
            for bgm in Bangumi.select():
                r.append(bgm)
        return r
    except Bangumi.DoesNotExist:
        return None
    finally:
        db.close()

def add( name, cur_epi=0, on_air_day=0, chk_key="" ):
    db.connect()
    bgm = Bangumi(name=name, cur_epi=cur_epi, on_air_day=on_air_day, chk_key=chk_key);
    bgm.save()
    db.close()

def modify( bid, name, cur_epi=0, on_air_day=0, chk_key="" ):
    db.connect()
    try:
        bgm = Bangumi.get(Bangumi.id==bid)
        bgm.name = name
        bgm.cur_epi = int(cur_epi)
        bgm.on_air_day = int(on_air_day)
        bgm.chk_key = chk_key
        bgm.save()
        return 1
    except Bangumi.DoesNotExist:
        return 0
    finally:
        db.close()

def remove(bid):
    db.connect()
    try:
        bgm = Bangumi.get(Bangumi.id==bid)
        bgm.delete_instance()
        return 1
    except Bangumi.DoesNotExist:
        return 0
    finally:
        db.close()

def plus( bid ):
    db.connect()
    try:
        bgm = Bangumi.get(Bangumi.id==bid)
        bgm.cur_epi = bgm.cur_epi +1
        bgm.save()
        return 1
    except Bangumi.DoesNotExist:
        return 0
    finally:
        db.close()

def decrease( bid ):
    db.connect()
    try:
        bgm = Bangumi.get(Bangumi.id==bid)
        bgm.cur_epi = bgm.cur_epi -1
        bgm.save()
        return 1
    except Bangumi.DoesNotExist:
        return 0
    finally:
        db.close()

def chkup( bid ):
    db.connect()

    try:
        bgm = Bangumi.get( Bangumi.id==bid  )
    except Bangumi.DoesNotExist:
        return 0
    else:
        tepi = bgm.cur_epi+1
        chkkey = str(bgm.chk_key) + " " + "%02d"%tepi
        # name = bgm.name
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
    finally:
        db.close()

