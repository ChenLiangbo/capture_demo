#!usr/bin/env/python 
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np

classfile = './haarcascades/haarcascade_frontalface_default.xml'
classfier = cv2.CascadeClassifier(classfile)

def read_images(path, newSize=None):
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
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            print "subdirname = ",subdirname
            subject_path = os.path.join(dirname, subdirname)
            print "subject_path = ",subject_path
            for filename in os.listdir(subject_path):
                try:
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    # im.shape = (112,92)
                    # resize to given size (if given)
                    if (newSize is not None):
                        im = cv2.resize(im, newSize)
                    if y.count(c) > 4:
                        pass
                    else:
                        #x_tmp = np.asarray(im, dtype=np.uint8)
                        #x_tmp.shape =  (112, 92)
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)         
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1       
        return [X,y]


def rawImageToFaceDataset(rawImageDirname,faceDatasetDirname,facesize = (92,112)):
    '''rawImageDirename = './ rawImage'  faceDatasetDirnaeme =  './faceDataset'
    '''
    imageNameList = os.listdir(rawImageDirname)
    dirnameList = []
    for imageName in imageNameList:
        filetext = os.path.splitext(imageName)
        name = filetext[0][:-2]
        if name not in dirnameList:
            dirnameList.append(name)    
    outdir = faceDatasetDirname
    for dirname in dirnameList:
        newDirname = outdir + '/' + dirname      
        isDir = os.path.isdir(newDirname)
        if isDir is False:
            os.mkdir(newDirname)
    
    cascadeClassfier = classfier
    for imageName in imageNameList:    
        filetext = os.path.splitext(imageName)
        name = filetext[0][:-2]                   # '.jpg'
        folderName = faceDatasetDirname + '/' + name + '/'
        imageOpenPath = rawImageDirname + '/' + imageName
        # imageSavePath = 'rawImageDirname/name/0.jpg'  example
        imageSavePath = folderName  +  filetext[0][-2:] +  filetext[1]   #imageName = "hg00.jpg" 
     
        image = cv2.imread(imageOpenPath)     

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#将当前桢图像转换成灰度图像
        cv2.equalizeHist(gray)                      #灰度图像进行直方图等距化 
        gray = cv2.GaussianBlur(gray,(5,5),0)

        faces = cascadeClassfier.detectMultiScale(gray, 1.3, 5) 
        if len(faces) > 0:
            face = faces[0]       # only one face on a photo
            (x,y,w,h) = face
            x1 = y - 10
            x2 = y + h + 10
            y1 = x - 10
            y2 = x + w + 10
            faceImage = image[x1:x2,y1:y2]
            try:
                faceImage = cv2.resize(faceImage,facesize,interpolation = cv2.INTER_CUBIC)
                cv2.imwrite(imageSavePath,faceImage)
            except Exception,ex:
                print "Exception:",ex
         


def getFaceToPredict(image):
    '''input a image with one face in BGR format,
    output a face image can be used in function faceRecognizer.facePredict '''
    if len(image.shape) == 3:    #BGRimage
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#将当前桢图像转换成灰度图像
    else:
        gray = image
    cv2.equalizeHist(gray)                      #灰度图像进行直方图等距化 
    gray = cv2.GaussianBlur(gray,(5,5),0)
    faces = classfier.detectMultiScale(gray,1.3,5)
    ret = {}
    flag = False
    if len(faces) > 0:
        if len(faces) > 1:
            print "[WARMING]The image have too many faces!!"
            return {"flag":flag,"face":None} 
        flag = True      
        (x,y,w,h) = faces[0]                   
        x1 = y - 10
        x2 = y + h + 10
        y1 = x - 10
        y2 = x + w + 10
        faceImage = gray[x1:x2,y1:y2] 
        try:
            faceImage = cv2.resize(faceImage,(92,112))
            ret['face'] = faceImage
            ret["flag"] = flag
        except Exception,ex:
            print "Exception:",ex
            ret["flag"] = False
            ret["face"] = None
        return ret        
    else:
        # print "[WARMING]Find no face in the image given!!"
        ret["face"] = None
        ret["flag"]  = flag
        return ret


## create facedataset
if __name__ =="__main__":
    '''test function and show example '''
    print "start prepare..."
    rawImageDirname = './faceImages'
    faceDatasetDirname = './faceDataset'
    rawImageToFaceDataset(rawImageDirname,faceDatasetDirname)
    
    path = '../../my_thesis/opencv/lyf3.jpg'
    image = cv2.imread(path)
    # print "type(image) = ",type(image)
    ret = getFaceToPredict(image)
    hasFace = ret["flag"]
    print "hasFace = ",hasFace
    face = ret["face"]
    # print "type(face) = ",type(face)
    print "face.shape = ",face.shape

  

    print "prepare finishied..."
