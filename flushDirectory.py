#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import os
import sys

try:
    flushdir = sys.argv[1]
except Exception,ex:
    print "Exception happens:",ex

fileList = os.listdir(flushdir)
count = 0
for f in fileList:
    filename = flushdir + '/' + f
    
    if ".py" not in f:
    	print "removing file--------",filename
        os.remove(filename)
        count = count + 1
    else:
        print "%s is a python demo,please remove it by hand!!" % (filename,)

print "removed %d files,it is finished!" % (count,)


