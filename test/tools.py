#!/usr/bin/env python
# coding=utf-8

from getPageRank import *
from getWhois import *


import re
from publicsuffix import PublicSuffixList


#url是否存在长词
def isHaveLongWord(url):
    url_list = url.split('.')

    for list in url_list:
        if len(list) >= 15:
            return 1

    return 0



#域名是否为纯长数字
def isHaveLongDigit(url):
    hostname = PublicSuffixList().get_public_suffix(url)


    m = re.match(r'\d*',hostname.split('.')[0])
    if m != None:
        if len(m.group()) >6:
            return 1

    
    return 0




#返回域名的特征向量
#特征1：PR值  int
#特征2：注册时间到现在的时间差 int
#特征3：URL点的个数是否>4 bool
#特征4：是否含有异常字符(!@~) bool
#特征5：url是否存在长词（>=15） bool
#特征6：域名是否为纯长数字（>6）
def getFeatureVector(hostName):
    vector = []
    
    vector.append( getBR(hostName) )
    #vector.append( query(hostName) )


    if len(hostName.split('.')) >= 4:
        vector.append(1)
    else:
        vector.append(0)


    if re.search(r'[~!@-]',hostName) != None:
        vector.append(1)
    else:
        vector.append(0)


    vector.append( isHaveLongWord(hostName) )
    vector.append( isHaveLongDigit(hostName) )

    return vector
