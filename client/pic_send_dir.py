#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import socket
import os
import time


HOST, PORT = "localhost", 1314
# HOST, PORT = "115.159.222.232", 1314
# HOST, PORT = "120.26.105.20", 1314
# HOST, PORT = "192.168.1.41", 1314 
try:
    model = os.sys.argv[1]
    imageDir = os.sys.argv[2]
    print "model = ",model
    print "imageDir = ",imageDir
except Exception,ex:
    print "Exception:",ex
    os.sys.exit()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect((HOST, PORT))  
except Exception,ex:
    print "Exception:",ex
    os.sys.exit()

icount = 0

sock.send(model)   # model1  model2  model3  model4  model5
data = sock.recv(10)

if data == '1':
    flag = True
    print "The server is ok,just go..."
else:
    flag = False
    "The server is busy,try agin later..."

number = int(3.5*1024)
try:
    while(flag):
        imageList = os.listdir(imageDir)
        if len(imageList) < 1:
            continue

        for f in imageList:
            if imageDir.endswith('/'):
                filename = imageDir + f
            else:
                filename = imageDir + './' + f
            if ('.jpg' not in f) and ('.png' not in f):
                continue
            icount = icount + 1
            print "sent image ------------",filename            
            sock.send('start') 
            fp = open(filename,'rb')
            file = fp.read(number)

            while (file):
                sock.send(file)
                file = fp.read(number)
                time.sleep(0.05)
            sock.send("end")
            os.remove(filename)
            data = sock.recv(10)

            if data == '1':
                flag = True
                print "The server is ok,just go..."
            else:
                flag = False
                "The server is busy,try agin later..."   
except Exception,ex:    
    print "Exception:",ex
    print "icount = ",icount
    sock.close()
    os.sys.exit()
   