#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
path = './_posts/'
if len(sys.argv) < 2:
    print 'defualt add to 30'
    linenum = 30
else:
    linenum = int(sys.argv[1])
    linenum = max(linenum, 10)
    linenum = min(linenum, 100)
    print "<!--more--> will be added to", linenum
for root , dirs, files in os.walk(path):
    for name in files:
        if name.endswith(".md"):
            print name
            name = path + name;
            fp = file(name)
            lines = []
            for line in fp: 
                if line != '<!--more-->\n':
                    lines.append(line)
            fp.close()
            
            lines.insert(linenum, '<!--more-->\n')
            s = ''.join(lines)
            fp = file(name, 'w')
            fp.write(s)
            fp.close()

