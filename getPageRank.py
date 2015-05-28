#!/usr/bin/env python
#coding=utf-8



import requests
import re
GPR_HASH_SEED ="Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE. Y\
es, I'm talking to you, scammer."



def google_hash(value):
    magic = 0x1020345
    for i in xrange(len(value)):
        magic ^= ord(GPR_HASH_SEED[i % len(GPR_HASH_SEED)]) ^ ord(value[i])
        magic = (magic >> 23 | magic << 9) & 0xFFFFFFFF
    return "8%08x" % (magic)



def getPR(www):
    try:
        url = 'http://toolbarqueries.google.com/tbr?' \
        'client=navclient-auto&ch=%s&features=Rank&q=info:%s' % (google_hash(www) , www)
        response = requests.get(url)
        rex = re.search(r'(.*?:.*?:)(\d+)',response.text)
        return rex.group(2)
    except :
        return None

def getBR(www):
    try:
        url = 'http://mytool.chinaz.com/baidusort.aspx?host=%s&sortType=0' % ( www,)
        response = requests.get(url)
        data = response.text
        rex = re.search(r'(<div class="siteinfo">.+?<font.+?>)(\d*?)(</font>)',data,re.I)
        return rex.group(2)
    except :
        return None

