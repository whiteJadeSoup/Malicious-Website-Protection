#!/usr/bin/env python
# coding=utf-8

def Domain_num_list(str):

    str = str.split(".")

    sum = 0
    sum_l = []

    for word in str:
        sum = 0
        #获取每一个域位的值
        for c in word:
            sum += ord(c)

        sum_l.append(sum)

    return sum_l


if __name__ == '__main__':
    s = "ferrulway.by"
    
    print Domain_num_list(s)
