#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import cv2
import numpy as np

source = '../image/cnt/'

print "test start..."
image = cv2.imread(source + 'source.jpg')
rawImage = image
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imwrite(source + 'gray.jpg',gray)

gray = cv2.GaussianBlur(gray,(5,5),0) 
cv2.imwrite(source + 'GaussianBlur.jpg',gray)

retVal,binary = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite(source + 'binary.jpg',binary)

kernel = np.ones((5,5),dtype = np.uint8)
opening = cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel)
cv2.imwrite(source + 'opening.jpg',opening)

contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print "len(contours) = ",len(contours)
cv2.drawContours(rawImage,contours,-1,(0,0,255),3)
cv2.imwrite(source + 'drawContours.jpg',rawImage)

# for i in range(len(contours)):
#     img = image
#     contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     print "drawContours --------",source + 'drawContours' + str(i) + '.jpg'
#     cv2.drawContours(img,contours[i],-1,(0,0,255),3)
#     cv2.imwrite(source + 'drawContours' + str(i) + '.jpg',img)
# cnt = contours[0]

print "test finishing..."
