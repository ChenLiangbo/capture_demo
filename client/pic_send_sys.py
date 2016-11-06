#!usr/bin/env/python 
# -*- coding: utf-8 -*-
import cv2
import socket
import time
import os
import sys

HOST, PORT = "localhost", 1314
# HOST, PORT = "115.159.222.232", 1314
# HOST, PORT = "120.26.105.20", 1314
# HOST, PORT = "192.168.1.41", 1314 
try:
    model = sys.argv[1]
except Exception,ex:
    print "Exception:",ex
    sys.exit()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect((HOST, PORT))  
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
t0 = time.time()
try:
    while(flag):    
        print "icount----------------------",icount
        icount = icount + 1    
        
        flag = cap.isOpened()
        if not flag:
            cap.open()
        ret, frame = cap.read()

        sock.send('start') 
        cv2.imwrite("./capture_image.jpeg",frame)
    
        f = open ("./capture_image.jpeg", "rb")   
        l = f.read(number)  
        while (l):  
            sock.send(l)  
            l = f.read(number)
            time.sleep(0.05)   

        sock.send('end')
        data = sock.recv(10)

        if data == '1':
            flag = True
            print "The server is ok,just go..."
        else:
            flag = False
            "The server is busy,try agin later..."   
except:
    t1 = time.time()
    print "icount = ",icount
    print "t1 - t0 = ",t1 - t0
    print "t = ",(t1-t0)/icount
    os.remove("./capture_image.jpeg")