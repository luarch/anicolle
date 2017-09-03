#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AniColle Library

Collect your animes like a geek.

Database model and operations here.
Unlike the previous version, this version returns objects as results rather than dictionaries by default.
You can force convert it into a dict by using to_dict().
"""

from peewee import *
from .seeker import seeker
from .config import config
import os
from json import loads as json_loads, dumps as json_dump

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
    name = TextField()                      # Bangumi name
    cur_epi = IntegerField(default=0)       # Currently viewing episode
    on_air_epi = IntegerField(default=0)    # (Placeholder)
    on_air_day = IntegerField(default=0)    # The on air weekday. [1-7] for Monday - Sunday, 0 for not on air, 8 for not fixed on air day.
    seeker = TextField(default='[]')
    '''
    Seeker is a modularized part of the program which is used to seek new episode of a bangumi programatically.
    Seekers are placed under `seeker` directory, and they are imported into this file as a dict named `seeker`.

    Seeker data saved in database is a serialized array (in json format), as following shows:
        [
            {
                "seeker": SEEKER_NAME,
                "chk_key": SEEKER_CHECK_KEY
            },
        ]

    chk_key is used for calling the `seek` function of 'seeker', usually a search keyword of the specific bangumi.
    For example, you want to download 'Tokyo Ghoul' from bilibili, then you should use "东京喰种" as a chk_key.
    For more information on `chk_key`, please refer to our wiki.
    '''
    class Meta:
        database = db

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cur_epi': self.cur_epi,
            'on_air_epi': self.on_air_epi,
            'on_air_day': self.on_air_day,
            'seeker': self.seeker
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
            for bgm in Bangumi.select().order_by(Bangumi.on_air_day):
                r.append(bgm.to_dict())
        return r
    except Bangumi.DoesNotExist:
        return None
    finally:
        db.close()

def create( name, cur_epi=0, on_air_day=0, seeker=[] ):
    db.connect()
    bgm = Bangumi(name=name, cur_epi=cur_epi, on_air_day=on_air_day, seeker=json_dump(seeker));
    bgm.save()
    db.close()
    return bgm.to_dict()

def modify( bid, name=None, cur_epi=None, on_air_day=None, seeker=None ):
    db.connect()
    try:
        bgm = Bangumi.get(Bangumi.id==bid)

        if name:
            bgm.name = name

        if cur_epi:
            bgm.cur_epi = int(cur_epi)

        if on_air_day:
            bgm.on_air_day = int(on_air_day)

        if seeker:
            bgm.seeker = json_dump(seeker)

        bgm.save()
        return bgm.to_dict()
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

def increase( bid ):
    db.connect()
    try:
        bgm = Bangumi.get(Bangumi.id==bid)
        bgm.cur_epi = bgm.cur_epi +1
        bgm.save()
        return bgm.cur_epi
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
        return bgm.cur_epi
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
            try:
                seek_result = seeker[seeker_seed['seeker']].seek(seeker_seed['chk_key'], bgm.cur_epi) # Maybe we need some new names. This can be confusable.
                if type(seek_result) == list:
                    r = r+seek_result
            except KeyError:
                print("[WARN] Seeker named", seeker_seed['seeker'] ,"not found. (Not registered?)")

        return r

        '''
         _/\_/\_/\_/\_/\_/\_/\_/\_
         End of checking module
        '''
    finally:
        db.close()

