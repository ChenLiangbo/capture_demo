#!usr/bin/env/python 
# -*- coding: utf-8 -*-
'''give image derectory and name
   can run anywhere
'''
import cv2

outdir = '../image/face/draw/'

classfier = cv2.CascadeClassifier('./haarcascade_mcs_upperbody.xml')

cap = cv2.VideoCapture(0)
iCount = 0
while(iCount < 40):
    flag = cap.isOpened()
    if not flag:
    	cap.open()
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(gray)     #灰度图像进行直方图等距化
    gray = cv2.GaussianBlur(gray,(5,5),0)
    objs = classfier.detectMultiScale(gray, 1.3, 5)     
    if len(objs) > 0:
        for (x,y,w,h) in objs:    
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            imageName = outdir + str(iCount) + '.jpg'  
        cv2.imwrite(imageName,frame)
        iCount = iCount + 1
        print "get body image number ---------------- ",iCount

print "finished testing..."