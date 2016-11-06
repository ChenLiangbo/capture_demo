#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import cv2
'''
MyCascadeClassfier includs FaceCascadeClassfier and BodyCascadeClassfier,has more function
BodyCascadeClassfier for body detection,includes upper body and lower body
FaceCascadeClassfier for face,eye,mouth detect
MyCascadeClassfier has the same function as combination of BodyCascadeClassfier and FaceCascadeClassfier
The reason why three classes is for vality,I want The Program more quiklier!
The smaller the class,the faster it is.[I have Tested!!] 
'''
class MyCascadeClassfier(object):
    """MyCascadeClassfier for Image classfier about face,eye,mouth,upperbody"""

    def __init__(self,bgrimage):
        super(MyCascadeClassfier, self).__init__()
        self.image = bgrimage      # should be given numpy.array(cv2 image)
        self.gray  = None          # gray image
        self.isPrepared = False    #transform bgrimage to gray
        self._faceClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')        
        self.faceNumber = 0       
        self._upperbodyClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_upperbody.xml')
        self.upperbodyNumber = 0
        self._lowerbodyClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_lowerbody.xml')
        self.lowerbodyNumber = 0
        self._eyeClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')
        self.eyeNumber = 0
        self._mouthClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_mouth.xml')
        self.mouthNumber = 0

    def prepareImage(self):
    	gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    	cv2.equalizeHist(gray)     #灰度图像进行直方图等距化
    	gray = cv2.GaussianBlur(gray,(5,5),0)
    	self.gray = gray
        self.isPrepared = True

    def findFace(self):
        if self.isPrepared is False:
            self.prepareImage()
        gray = self.gray
    	classfier = self._faceClassfier
    	faces = classfier.detectMultiScale(gray, 1.3, 5)
    	number = len(faces)    
        self.faceNumber = number

    def findUpperbody(self):
        if self.isPrepared is False:
            self.prepareImage()
        gray = self.gray
    	classfier = self._upperbodyClassfier
    	upperbodies = classfier.detectMultiScale(gray,1.3,5)
    	number = len(upperbodies)
        self.upperbodyNumber = number   

    def findLowerbody(self):
        if self.isPrepared is False:
            self.prepareImage()
        gray = self.gray
        classfier = self._lowerbodyClassfier
        lowerbodies = classfier.detectMultiScale(gray,1.3,5)
        self.lowerbodyNumber = len(lowerbodies)

    def findEye(self):
        if self.isPrepared is False:
            self.prepareImage()
        eyes = self._eyeClassfier.detectMultiScale(self.gray)
        self.eyeNumber = len(eyes)

    def findMouth(self):
        if self.isPrepared is False:
            self.prepareImage()
        mouthes = self._mouthClassfier.detectMultiScale(self.gray,1.3,5)


class BodyCascadeClassfier(object):
    '''cascade classfier for body,including upper body and lower body'''
    def __init__(self):
        super(BodyCascadeClassfier, self).__init__()      
        self.gray  = None          # gray image
        self.isPrepared = False    #transform bgrimage to gray
        self._upperbodyClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_upperbody.xml')
        self.upperbodyNumber = 0
        self._lowerbodyClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_lowerbody.xml')
        self.lowerbodyNumber = 0

    def prepareImage(self,image):
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(gray)     #灰度图像进行直方图等距化
        gray = cv2.GaussianBlur(gray,(5,5),0)
        self.gray = gray
        self.isPrepared = True


    def findUpperbody(self):
        if self.isPrepared is False:
            return None
        gray = self.gray
        classfier = self._upperbodyClassfier
        upperbodies = classfier.detectMultiScale(gray,1.3,5)
        number = len(upperbodies)
        self.upperbodyNumber = number   

    def findLowerbody(self):
        if self.isPrepared is False:
            self.prepareImage()
        gray = self.gray
        classfier = self._lowerbodyClassfier
        lowerbodies = classfier.detectMultiScale(gray,1.3,5)
        self.lowerbodyNumber = len(lowerbodies)

#quikler
class FaceCascadeClassfier(object):
    '''cascade classfier for face,including face detect,eye,and mouth'''


    def __init__(self,BGRimage):
        super(FaceCascadeClassfier, self).__init__()
        self.image = BGRimage      # should be given numpy.array(cv2 image)
        self.gray  = None          # gray image
        self.isPrepared = False    #transform bgrimage to gray
        self._faceClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')        
        self.faceNumber = 0  
        self._eyeClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')
        self.eyeNumber = 0
        self._mouthClassfier = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_mouth.xml')
        self.mouthNumber = 0

    def prepareImage(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(gray)     #灰度图像进行直方图等距化
        gray = cv2.GaussianBlur(gray,(5,5),0)
        self.gray = gray
        self.isPrepared = True

    def findFace(self):
        if self.isPrepared is False:
            self.prepareImage()
        gray = self.gray
        classfier = self._faceClassfier
        faces = classfier.detectMultiScale(gray, 1.3, 5)
        number = len(faces)    
        self.faceNumber = number

    def findEye(self):
        if self.isPrepared is False:
            self.prepareImage()
        eyes = self._eyeClassfier.detectMultiScale(self.gray,1.3,5)
        self.eyeNumber = len(eyes)

    def findMouth(self):
        if self.isPrepared is False:
            self.prepareImage()
        mouthes = self._mouthClassfier.detectMultiScale(self.gray,1.3,5)


#examples and velocity test
if __name__ == "__main__":
    
    import time
    t0 = time.time()
    image = cv2.imread('../../my_thesis/opencv/lyf3.jpg')
    print "type(image) = ",type(image)

    t1 = time.time()
    print "t1 - t0 = ",t1 - t0
    
    myCascadeClassfier = BodyCascadeClassfier()
    
    t2 = time.time()
    print "t2 - t1 = ",t2 - t1
    myCascadeClassfier.prepareImage(image)
    myCascadeClassfier.findUpperbody()
    bodyNumber = myCascadeClassfier.upperbodyNumber
    print "bodyNumber = ",bodyNumber

    # print "upperbodyNumber = ",myCascadeClassfier.upperbodyNumber
    # # t3 = time.time()
    # print "t3 - t2 = ",t3 - t2
    # myCascadeClassfier.findFace()
    # print "faceNumber = ",myCascadeClassfier.faceNumber
    
    myCascadeClassfier.findLowerbody()
    print "lowerbodyNumber = ",myCascadeClassfier.lowerbodyNumber
    
    # myCascadeClassfier.findEye()
    # print "eyeNumber = ",myCascadeClassfier.eyeNumber
    
    # t4 = time.time()
    # print "t4 - t3 = ",t4 - t3
    # print "t4 - t0 = ",t4 - t0
    print "It is ok!"
  