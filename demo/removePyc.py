#!user/bin/env/python

import os
import sys


filedir = sys.argv[1]

print "filedir = ",filedir

fileList = os.listdir(filedir)

for f in fileList:
    if (".pyc" in f) or (".py~" in f):
        filename = filedir + '/' + f
        print "removed file:",filename
        os.remove(filename)

print "Remove okay!"
        
