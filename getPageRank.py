#!/usr/bin/env python

# Google Pagerank Checksum Algorithm (Firefox Toolbar)
# Downloaded from http://pagerank.phurix.net/
# Requires: Python >= 2.4

# Versions:
# pagerank2.py 0.2 - Fixed a minor formatting bug
# pagerank2.py 0.1 - Public release


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
    except Exception, e:
        print e
        return None

def getBR(www):
    try:
        url = 'http://mytool.chinaz.com/baidusort.aspx?host=%s&sortType=0' % ( www,)
        response = requests.get(url)
        data = response.text
        rex = re.search(r'(<div class="siteinfo">.+?<font.+?>)(\d*?)(</font>)',data,re.I)
        return rex.group(2)
    except Exception,e:
        return 0

if __name__ == "__main__" :
    print getPR("www.7k7k.com")
