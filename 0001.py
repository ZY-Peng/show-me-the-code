#-*- coding:utf-8 -*-

import uuid
import random,string

def CreateByUUID(Count=10):
    codeset=set()
    while len(codeset)<Count:
        codeset.add(str(uuid.uuid4()).replace('-','').upper())
    for code in codeset:
        print(code)

def CreateByRandom(Round=15,Count=10):
    ALL_LETTERS = string.ascii_uppercase + string.digits
    codeset=set()
    while len(codeset) < Count:
        onecode=''.join((random.choice(ALL_LETTERS) for i in range(Round)))
        codeset.add(onecode)
    for code in codeset:
        print(code)

print("使用UUID生成随机数：")
CreateByUUID()
print("使用Random生成随机数：")
CreateByRandom()
