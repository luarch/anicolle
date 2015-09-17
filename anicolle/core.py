#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AniColle Library

Collect your animes like a geek.

Database model and operations here.
Unlike the previous version, this version returns objects as results rather than dictionaries by default.
You can force convert it into a dict by using to_dict().
"""

from peewee import *
from .seeker import seeker
from .config import config
import os
from json import loads as json_loads

run_mode = os.getenv('ANICOLLE_MODE') or 'default'
try:
    config = config[run_mode]
    # print("Running with", run_mode, "mode")
except KeyError :
    print("No such running mode. Check your ANICOLLE_MODE system env please.")
    exit()

db = SqliteDatabase(config.DATABASE)

class Bangumi(Model):
    # `id` field is added automatically
    name = TextField()
    cur_epi = IntegerField(default=0)
    on_air_epi = IntegerField(default=0)
    on_air_day = IntegerField(default=0)
    seeker = TextField(default='[{"seeker": "popgo", "chk_key": ""}]')
    class Meta:
        database = db

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cur_epi': self.cur_epi,
            'on_air_epi': self.on_air_epi,
            'on_air_day': self.on_air_day,
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
            r = Bangumi.get(Bangumi.id==bid).to_dict()
        elif on_air_day>=0:
            # get a set of records
            for bgm in Bangumi.select().where(Bangumi.on_air_day==on_air_day):
                r.append(bgm.to_dict())
        else:
            # get all records
            for bgm in Bangumi.select():
                r.append(bgm.to_dict())
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

def modify( bid, name=None, cur_epi=None, on_air_day=None, chk_key=None ):
    db.connect()
    try:
        bgm = Bangumi.get(Bangumi.id==bid)

        if name:
            bgm.name = name

        if cur_epi:
            bgm.cur_epi = int(cur_epi)

        if on_air_day:
            bgm.on_air_day = int(on_air_day)

        if chk_key:
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
        '''
        Start of checking module
        \/_\/_\/_\/_\/_\/_\/_\/_\/
        '''

        r = []

        bgm_seeker_data = json_loads(bgm.seeker);

        for seeker_seed in bgm_seeker_data:
            r.append(seeker[seeker_seed['seeker']].seek(seeker_seed['chk_key'], bgm.cur_epi))    # Maybe we need some new names. This can be confusable.

        return r

        '''
         _/\_/\_/\_/\_/\_/\_/\_/\_
         End of checking module
        '''
    finally:
        db.close()

