#!usr/bin/env/python 
# -*- coding: utf-8 -*-
'''give image derectory and name
   can run anywhere
'''
import cv2
import numpy as np

classfier = cv2.CascadeClassifier('./haarcascade_mcs_upperbody.xml')
image = cv2.imread('../image/body/ori.jpg')
img = image

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('../image/body/gray.jpg',gray)
cv2.equalizeHist(gray)     #灰度图像进行直方图等距化

cv2.imwrite('../image/body/equalizeHist.jpg',gray)
gray = cv2.GaussianBlur(gray,(5,5),0)
cv2.imwrite('../image/body/GaussianBlur.jpg',gray)

objs = classfier.detectMultiScale(gray, 1.3, 5) 
print "faces = ",objs
print "len(faces) = ",len(objs)
    
if len(objs) > 0:
    for (x,y,w,h) in objs:    
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)            
        # x1 = y - 10
        # x2 = y + h + 10
        # y1 = x - 10
        # y2 = x + w + 10
        # faceImage = img[x1:x2,y1:y2]
cv2.imwrite('../image/body/finder.jpg',img)
print "finished testing..."