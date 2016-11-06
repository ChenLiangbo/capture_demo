#!usr/bin/env/python 
# -*- coding: utf-8 -*-
'''test get face from capture
   save original image,prepared image and retangula face image
   only after moving this demo to directory capture/server can it run
'''
import cv2
import numpy as np
import time

personName = "chenliangbo"
oridir = '../test/image/face/ori'
getdir = '../test/image/face/get'
predir = '../test/image/face/pre'
iCount = 0
classfier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)

print "start taking face photo..."
iCount = 0
while(iCount < 20):
    flag = cap.isOpened()
    if not flag:
    	cap.open()
    ret, frame = cap.read()
    oriImage = frame
    if iCount < 10:
            imageName1 = oridir + '/' + personName + '0' + str(iCount) + '.jpg'
    else:
            imageName1 = oridir + '/' + personName + str(iCount) + '.jpg'
    

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(gray)     #灰度图像进行直方图等距化
    gray = cv2.GaussianBlur(gray,(5,5),0)
    faces = classfier.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        cv2.imwrite(imageName1,oriImage)
        print "imageName1 = ",imageName1
        face = faces[0]
    	print "get a good face image ----------",iCount
        if iCount < 10:
    	    imageName2 = predir + '/' + personName + '0' + str(iCount) + '.jpg'
        else:
            imageName2 = predir + '/' + personName + str(iCount) + '.jpg'
    	cv2.imwrite(imageName2,gray) 
        (x,y,w,h) = face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)   	 
    	iCount = iCount + 1
        cv2.imshow('frame',frame)
        if iCount < 10:
            imageName3 = getdir + '/' + personName + '0' + str(iCount) + '.jpg'
        else:
            imageName3 = getdir + '/' + personName + str(iCount) + '.jpg'
        cv2.imwrite(imageName3,frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        time.sleep(1)
        iCount = iCount + 1
	
# Release everything if job is finished
cap.release()

cv2.destroyAllWindows()

print "It is okay!"
