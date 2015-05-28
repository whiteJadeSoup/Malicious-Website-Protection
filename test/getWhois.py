#coding=utf-8
import urllib
import re
import datetime




def str_cut(str,startsep,endsep):
    str1=str.split(startsep)[1]
    str2=str1.split(endsep)[0]
    return str2
 

def whois(host):
      url='http://whois.chinaz.com/'+host
      data=urllib.urlopen(url).read()

      print data
      if data.find('<div id="whoisinfo" class="div_whois">')==-1:
          data=0
      else:
          data=str_cut(data,'<div id="whoisinfo" class="div_whois">','</div>')
          data=data.replace('<br/>','\n')
      return data
 

def getTimeDifference(data):
    #获取时间
    index = data.find('过期')
    index = data.find('：',index)


    rindex = data.rfind('：',0,index)
    data = data[rindex+3:data.find('\n',rindex)]

    datas = []
    d1 = None
    d2 = datetime.date.today()


    if data.find('年') != -1:
        datas.append(data[0:4])

        #print data[0:4]
        datas.append(data[7:9])
        #print data[7:9]
        datas.append(data[12:14])
        #print data[12:14]

        try:
            d1 = datetime.date(int(datas[0]),int(datas[1]),int(datas[2]))
        except:
            return 0
    else:

        index = data.find(" ",1)
        try:
            d1 = datetime.datetime.strptime(data[1:index], "%Y-%m-%d").date()
        except:
            return 0


    #print d2
    #print d1
    return (d2-d1).days



def query(host):

   host=host.lower()
   data=whois(host)
   return getTimeDifference(data)
