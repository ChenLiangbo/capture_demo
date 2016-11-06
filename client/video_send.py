#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import socket
import time
import os

HOST, PORT = "localhost", 1314
# HOST, PORT = "115.159.222.232", 1314
# HOST, PORT = "120.26.105.20", 1314

videoDir = './'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect((HOST, PORT)) 

sock.send('model1')   # model1  model2  model3  model4  model5
data = sock.recv(10)

if data == '1':
    flag = True
    print "The server is ok,just go..."
else:
    flag = False
    "The server is busy,try agin later..."

number = int(3.5*1024)
while (True):
    videoList = os.listdir(videoDir)
    if len(videoList) < 1:
	continue

    for f in videoList:    
        if '.avi' not in f:
            print "f = ",f
            continue
        videoName = videoDir + '/' + f
        print "sending video -------- ",videoName
        cap = cv2.VideoCapture(videoName)
        ret, frame = cap.read()
    
        while(ret and flag):
            ret, frame = cap.read()
            sock.send('start') 
            cv2.imwrite("./capture_image.jpg",frame)    
            f = open ("./capture_image.jpg", "rb")   
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
        ret = True  
        os.remove(videoName)
sock.close()
os.remove("./capture_image.jpg")

