#!usr/bin/env/python 
# -*- coding: utf-8 -*-
'''find person from video
   save save video pice about three or four second from given video when find person
'''
import cv2
import os

ouputPath = '../finder/'
try:
	filename = os.sys.argv[1]
except Exception,ex:
    print "Exception:",ex
    os.sys.exit() 

classfier1 = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_upperbody.xml')
classfier2 = cv2.CascadeClassifier('./haarcascades/haarcascade_lowerbody.xml')


videoName = filename
dirPath,filename = os.path.split(filename)
dirName,avi = os.path.splitext(filename)
print dirName,avi

fourcc = cv2.cv.FOURCC(*'XVID')
frameFrequency = 25.0
frameSize = (640,480)
frameNumber = 100

frameCount = 0
finderCount = 0
personFlag = False

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print "ret = ",ret

while(ret):
    print "frameCount -------------- ",frameCount
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.equalizeHist(gray)     #灰度图像进行直方图等距化
    gray = cv2.GaussianBlur(gray,(5,5),0)
    upperbodies = classfier1.detectMultiScale(gray,1.3,5)
    personNumber = len(upperbodies)
    if personNumber < 1:
        upperbodies = classfier2.detectMultiScale(gray,1.3,5)
        personNumber = len(upperbodies)
    else:
        personFlag = True
    if (personNumber < 1) and (not personFlag):
        continue
    if frameCount == 0:
       	print "finder video number --------",finderCount
        if not os.path.exists(ouputPath + dirName):
            os.mkdir(ouputPath + dirName)
        outputName = ouputPath + dirName + '/' + str(finderCount) + avi
        outWriter = cv2.VideoWriter(outputName,fourcc, frameFrequency,frameSize)
        finderCount = finderCount + 1
    outWriter.write(frame)
    frameCount = frameCount + 1

    if frameCount == frameNumber:
        outWriter.release()
    	frameCount = 0
    	personFlag = False
    ret, frame = cap.read()
print "finder finished ..."
outWriter.release()
