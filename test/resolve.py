#!/usr/bin/env python
# coding=utf-8


flag = ['\x02','\x03','\x04','\x05','\x06','\x07','\x1a','\x11','\x1d']

def replaceWithDoct(string):
    
    if string in flag:
        return '.'
    #print 'call doct'
    return string


def getHostName(string):
    begin = 0
    before = 0

    print '现在处理的字符串是:' + string
    print len(string)
    for s in string:
        if s == '\x00':
            index = string.find(s,before) +1
            before = index 
            print '索引：' + str(index)
            if index != -1:
              if index == len(string):
                break;
              if string[index] in flag:
                begin = index + 1
                break

    end = string.find('\x00',begin)

    name = string[begin+1:end]
    
    name = "".join(map(replaceWithDoct,name))
    docIndex = name.find('com')

    return name[:docIndex-1] + '.' + name[docIndex:]
