#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import redis
import uuid

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379


def CreateByUUID(Count=10):
    codeset=set()
    while len(codeset)<Count:
        codeset.add(str(uuid.uuid4()).replace('-','').upper())
    return codeset

conn= redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
for code in CreateByUUID():
    conn.sadd('CodeSet',code)
CodeSet = conn.smembers('CodeSet')
print("从Redis中读取")
for code in CodeSet:
    print(code)
