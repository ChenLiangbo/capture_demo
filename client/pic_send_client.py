#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import socket
import time

HOST, PORT = "localhost", 1314
# HOST, PORT = "192.168.1.41", 1314 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect((HOST, PORT))  

sock.send('model1')   # model1  model2  model3  model4  model5
data = sock.recv(1024)

if data == '1':
    flag = True
    print "The server is ok,just go..."
    time.sleep(0.5)
else:
    flag = False
    "The server is busy,try agin later..."
icount = 0
while(icount < 100):    
    print "icount----------------------",icount
    icount = icount + 1      
    sock.send('start')
   
    f = open ("./capture_image.jpg", "rb")   
    l = f.read(1024*32)  
    while (l):  
        sock.send(l)  
        l = f.read(1024*32)
        time.sleep(0.05)
        
    # time.sleep(0.4)    

    sock.send('end')
    data = sock.recv(1024)

    if data == '1':
        flag = True
        print "The server is ok,just go..."
    else:
        flag = False
        "The server is busy,try agin later..."
    time.sleep(0.05)

sock.close()
