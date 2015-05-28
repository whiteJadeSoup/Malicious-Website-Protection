#!/usr/bin/env python
# coding=utf-8


if __name__ == '__main__':
    index = 1

    f = open('target.txt','w')
    while index <= 200:
        if index <= 100:
            f.write('0\n')

        else:
            f.write('1\n')

        index += 1
