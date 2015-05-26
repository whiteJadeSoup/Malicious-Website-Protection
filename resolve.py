#!/usr/bin/env python
# coding=utf-8


flag = ['\x02','\x03','\x04','\x05','\x06','\x07','\x1a','\x11']

def replaceWithDoct(str):
    
    if str in flag:
        return '.'
    #print 'call doct'
    return str


def getHostName(str):
    begin = 0
    before = 0

    for s in str:
        if s == '\x00':
            index = str.find(s,before) + 1
            before = index
            if str[index] in flag:
                begin = index + 1
                break

    end = str.find('\x00',begin)

    name = str[begin:end]
    
    name = "".join(map(replaceWithDoct,name))
    docIndex = name.find('com')

    return name[:docIndex-1] + '.' + name[docIndex:]
