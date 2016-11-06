#!usr/bin/env/python 
# -*- coding: utf-8 -*-
import cv2
import os
import time


print "program start..."
obj_cascade = cv2.CascadeClassifier('./xmlfile/haarcascade_frontalface_default.xml')

imagedir = './faceImages'
fileList = os.listdir(imagedir)
iHuge = 0
iLiuyifei = 0
for imageFile in fileList:   
    imageName = imagedir+'/'+imageFile
    print "imageName = ",imageName
    splitName = os.path.splitext(imageFile)
    print "splitName = ",splitName      # 0 is file  1 is .jpg
    img = cv2.imread(imageName)
    # print "img.shape = ",img.shape
    # newSize = (200,200) 
    # img1 = cv2.resize(img,newSize,interpolation=cv2.INTER_CUBIC)  
  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#将当前桢图像转换成灰度图像
    cv2.equalizeHist(gray)                      #灰度图像进行直方图等距化 
    gray = cv2.GaussianBlur(gray,(5,5),0)

    objs = obj_cascade.detectMultiScale(gray, 1.3, 5) 
    print "faces = ",objs
    print "len(faces) = ",len(objs)
    
    if len(objs) > 0:
        print "imageFile = ",imageFile
        for (x,y,w,h) in objs:
            # img1 = img.copy()
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)            
            x1 = y - 10
            x2 = y + h + 10
            y1 = x - 10
            y2 = x + w + 10
            faceImage = img[x1:x2,y1:y2]
            # print "type(faceImage) = ",type(faceImage)
         
            # roi_gray = gray[y:y+h, x:x+w]
            # roi_color = img[y:y+h, x:x+w]
            # eyes = eye_cascade.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in eyes:
            #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)           
            cv2.imshow("Image", img)
            cv2.imshow("faceImage",faceImage)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                continue
            time.sleep(1)

    # cv2.imshow("Image", img)
    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #     continue

# cv2.rectangle(img,(0,0),(100,100),(0,0,255),2)


cv2.destroyAllWindows()
    

print"It is ok!"

