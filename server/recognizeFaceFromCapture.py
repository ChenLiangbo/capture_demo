#!usr/bin/env/python 
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import json
import time
from trainFaceRecognizerModel import MyFaceRecognizer
from  updateFaceDataset import getFaceToPredict


faceRecognizer = MyFaceRecognizer()
faceRecognizer.modelSavedFile = './xmlfile/faceModel.xml'
faceRecognizer.loadModel()

labelsJson = open('./xmlfile/labels.txt','r').read()
labelsDict = json.loads(labelsJson)
print "labelsDict = ",labelsDict

cap = cv2.VideoCapture(0)

while(True):
    flag = cap.isOpened()
    if not flag:
    	cap.open()
    ret, frame = cap.read()
    faceResult = getFaceToPredict(frame)
    faceFlag = faceResult["flag"]
    if faceFlag == True:
        face = faceResult["face"]
        # print "face.shape = ",face.shape
        recognizeResult = faceRecognizer.facePredict(face)
        # print "recognizeResult = ",recognizeResult
        label = recognizeResult["label"]
        # print "label = ",type(label)
        if str(label) in labelsDict:
            print "The person is------- ",labelsDict[str(label)]
            # time.sleep(2)

    # faceRecognizer.facePredict()
    cv2.imshow('frame',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
	
cap.release()
cv2.destroyAllWindows()

