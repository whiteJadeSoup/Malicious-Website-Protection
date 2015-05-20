#!/usr/bin/env python
# coding=utf-8



if __name__ == '__main__':
    fn = open("feature.txt","w")

    with open("file.txt",'r') as f:
        for line in f.readlines():
            line = line.strip()
            line_split = line.split(".")

            #print(line_split)

            sum = 0
            string = ""
            for domain in line_split:
                #print(domain)

                for c in domain:
                    sum += ord(c)

                string += (str(sum) + ',')
                #print(string)

            string = string[0:-1]
            #print (string.split(","))

            if len(string.split(',')) == 2:
                string += ",0"

            fn.write(string)
            fn.write("\n")

    fn.close()


