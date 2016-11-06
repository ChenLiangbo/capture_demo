#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import datetime

videoDir = "./"
cap = cv2.VideoCapture(0)
fourcc = cv2.cv.FOURCC(*'XVID')
now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
videoName = videoDir + 'VID' + now + '.avi'
outWriter = cv2.VideoWriter(videoName,fourcc, 25.0, (640,480))
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        outWriter.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
    	break

outWriter.release()
cv2.destroyAllWindows()
