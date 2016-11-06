#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import cv2
import cv2.cv as cv
import numpy as np

faceClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
upperbodyClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_upperbody.xml')


def prepareToDetect(BGRimage):
    gray = cv2.cvtColor(BGRimage, cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(gray)     #灰度图像进行直方图等距化
    gray = cv2.GaussianBlur(gray,(5,5),0)
    return gray


def faceDetect(gray):
    #input cv2 image ,numpy.array
    #if there is face,return True,else,False	
	faces = faceClassfier.detectMultiScale(gray, 1.3, 5)
	flag = False
	if len(faces) > 0:
		flag = True
	return flag

def upperbodyDetect(gray):    
    upperbodies = upperbodyClassfier.detectMultiScale(gray,1.3,5)
    flag = False
    if len(upperbodies) > 0:
        flag = True
    return flag

def findCentroid(image):
    #input bgr image,numpy.array
    #return centroid

    img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray,(5,5),0) 

    retVal,binary = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = np.ones((5,5),dtype = np.uint8)
    opening = cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel)
    

    contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]

    M = cv2.moments(cnt)

    cx = int(M['m01']/M['m00'])
    cy = int(M['m01']/M['m00'])

    area = cv2.contourArea(cnt)

    centroid = (cx,cy)
    ret = [centroid,area]
    return  ret

def videoTransform(filename):
    #transform avi video to mp4 video
    #if video is './video.avi',then filename = './video'
    file1 = filename + '.avi'
    file2 = filename + '.mp4'

    fp1 = open(file1,'rb')
    fp2 = open(file2,'wb')

    data = fp1.read(1024*10)
    while data:
        fp2.write(data)
        data = fp1.read(1024*10)
    fp1.close()
    fp2.close()
    return file2


def get_cv2_image(self,filename):
        if self.hasImage is True:
            image = cv2.imread(filename)
            if type(image) == 'numpy.ndarray':
                return image
            else:
                return None
        else:
            print "open image erro:no image file..."
            return None

if __name__ == '__main__':

    img = cv2.imread('./positive 0.jpg')
    flag = faceDetect(img)
    print "flag = ",flag
    centroid_area = findCentroid(img)
    print "centroid = ",centroid_area[0]           #tuple
    print "area = ",centroid_area[1]               #float
    print "It is ok!"
