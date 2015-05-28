#!/usr/bin/env python
# coding=utf-8

from tools import *



def Website2Vector():
    website_f = open('w.txt','r')
    feature_f = open('feature.txt','w')
    for line in website_f.readlines():
        vector = getFeatureVector(line)
        print vector

        index = 0
        for v in vector:
          if index != len(vector)-1:
            feature_f.write(str(v)+' ')
          else:
            feature_f.write(str(v))
          index += 1
        
        feature_f.write('\n')

    website_f.close()
    feature_f.close()



if __name__ == '__main__':
    Website2Vector()

