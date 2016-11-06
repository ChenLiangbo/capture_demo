#!usr/bin/env/python 
# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
import json

class MyFaceRecognizer(object):
    '''For Face Recognizer'''
    def __init__(self):
        super(MyFaceRecognizer, self).__init__()
        # self.model = cv2.createEigenFaceRecognizer()
        self.model = cv2.createLBPHFaceRecognizer()     # most rate of right
        # model = cv2.createFisherFaceRecognizer()
        self.isTrained = False      # model is trained or not
        self.modelSavedFile = ''    #model save file .xml file
        self.XimageList = []        #images for train
        self.yLabelList = []        #image label
       
    def trainModel(self):
    	'''X1 list,item is gray image, y1 is list,item is np.int32'''
    	X1 = np.asarray(self.XimageList)  #X1.shape =  (200, 112, 92)
        y1 = np.asarray(self.yLabelList,dtype = np.int32)  #y1.shape =  (200,)        
        self.model.train(X1,y1)
        self.isTrained = True
        if self.modelSavedFile:
            f = open(self.modelSavedFile,'w')
            self.model.save(self.modelSavedFile)
            self.isModelSaved = True

    def loadModel(self):
        if self.isTrained == False:
            self.model.load(self.modelSavedFile)
            self.isTrained = True

    def facePredict(self,img):
    	'''img.ndim = 2'''
    	if self.isTrained == False:
            self.trainModel()
    	[p_label, p_confidence] = self.model.predict(img)
    	predictResult = {}
    	predictResult["confidence"] = p_confidence
    	predictResult["label"] = p_label
    	return predictResult

    def precisionTest(self):
    	if self.isTrained == False:
    	    self.trainModel()
    	number = len(self.XimageList)
    	correctNumber = 0
    	X = self.XimageList
    	for i in range(number):
    	    [p_label,p_confidence] = self.model.predict(X[i])
            if p_label == self.yLabelList[i]:
                correctNumber = correctNumber + 1
    	testResult = float(correctNumber)/number
    	print "Test %d face images,and %d of them are right..." % (number,correctNumber)
    	return testResult
        

    def read_images(self,path, newSize=None):
        """从文件夹中读取图像，并且将其大小限制在一定范围之内
        参数:
            path: 图片的路径
            sz: 设定图像的大小以元组的形式，例如(92,112)
        返回值:
            返回一个list的数据[X,y]
            X: 一个numpy的数组，里面存储的是所有的图片的矩阵.
            y:一个list存储的，都是与X中图片对应的lable
        """
        c = 0
        X,y = [], []
        labelsDict = {}
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                labelsDict[c] = subdirname
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    try:
                        im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)  
                        if (newSize is not None):
                            im = cv2.resize(im, newSize)                   
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)         
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
                c = c+1
        self.XimageList = X
        self.yLabelList = y
        labelsJson = json.dumps(labelsDict)
        with open('./xmlfile/labels.txt','w') as f:
            f.write(labelsJson)
        f.close()
        return [X,y]



##example and program test
#train the model and save it
if __name__ =='__main__':   
    print "test start..."

    faceRecognizer = MyFaceRecognizer() 
      
    path = './faceDataset'
    [X,y] = faceRecognizer.read_images(path)
    print "number of  face Sample = ",len(X)
    print "faceShape = ",X[0].shape

    labelsJson = open('./xmlfile/labels.txt','r').read()
    labelsDict = json.loads(labelsJson)
    print "labels = ",labelsDict
    # print "labelsDict['1'] = ",labelsDict['1']    
    
    #save model as modelSavedFile
    modelSavedFile = './xmlfile/faceModel.xml'
    faceRecognizer.modelSavedFile = modelSavedFile

    # faceRecognizer.loadModel()       # load from modelSavedFile
    faceRecognizer.trainModel()       # train model
    print "model train okay ..."
    faceRecognizer.precisionTest()
    print "model test okay ..."

    ret = faceRecognizer.facePredict(X[5])
    print "ret = ",ret
    label = ret["label"]
    predictName = labelsDict[str(label)]
    print "predict result:predictName = ",predictName

    print "test end..."


        

    
