#!usr/bin/env/python 
# -*- coding: utf-8 -*-
import cv2
import os

from cascadeClassfier import BodyCascadeClassfier      # for body detect

print "start testing..."
cascadeClassfier = BodyCascadeClassfier()     # find upperbody and lowerbody class

datadir = '../test/pedestrians128x64'
datadir = '../test/USCPedestrianSetA'

'''
http://blog.csdn.net/pb09013037/article/details/41651279
1,MIT数据库 -Pedestrian Data-- http://cbcl.mit.edu/software-datasets/PedestrianData.html
2,Caltech行人数据库 -Caltech Pedestrian Detection Benchmark--http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians/
3,USC行人数据库 USC-A|-USC Pedestrian Detection Test Set --http://iris.usc.edu/Vision-Users/OldUsers/bowu/DatasetWebpage/dataset.html
'''

fileList = os.listdir(datadir) 

totalNumber =  0


number = 0
for f in fileList:
    if ('.bmp' in f) or ('.jpg' in f):	
	    filename = datadir + '/' + f
	    print "filename = ",filename
	    totalNumber = totalNumber + 1
	    frame = cv2.imread(filename)
	    cascadeClassfier.prepareImage(frame)
	    cascadeClassfier.findUpperbody()
	    bodyNumber = cascadeClassfier.upperbodyNumber
	    if bodyNumber > 0:
		    number = number + 1

print "bodyNumber = ",number
print "rate = ",float(totalNumber)/number
print "finished testing ..."