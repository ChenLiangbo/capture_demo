#!usr/bin/env/python 
# -*- coding: utf-8 -*-
from twisted.internet import reactor                     #twsited
from twisted.internet.protocol import Protocol, Factory  #twsited
from twisted.python import log                           #twsited
import cv2                         # image module
import numpy as np                 # image and math module
import datetime                    # image and video save and for log
import sys                         # for log
import os
import math                        # sqrt 
import json                        # for label
import time                        # for time test
from mychat import mychat          # my own file for wechat message sending
import imageFunction               # my own image function module
from cascadeClassfier import BodyCascadeClassfier      # for body detect
from trainFaceRecognizerModel import MyFaceRecognizer  # for face recognize
from updateFaceDataset import getFaceToPredict         # for detect face


cascadeClassfier = BodyCascadeClassfier()     # find upperbody and lowerbody class

faceRecognizer  =  MyFaceRecognizer()         # face recognizer class
modelSavedFile = './xmlfile/faceModel.xml'
faceRecognizer.modelSavedFile = modelSavedFile
faceRecognizer.loadModel()       # load from modelSavedFile
labelsJson = open('./xmlfile/labels.txt','r').read()   # person name label
labelsDict = json.loads(labelsJson)                    # to a dict

# 定义你Protocol类
class SimpleProtocol(Protocol):

    timeout = 1000

    def __init__(self):            
        self.hasImage  = False
        self.imageFile = ''                       #to store image binary stream from socket
        self.imageDir  = '../images/'              #the path saving picture
        self.videoDir  = '../video/'
        self.imageName = ''
        self.frameCount = 0                       #to count picture recieve
        self.outWriter = None                     #cv2 objects to store video
        self.isImage   = False    # model1 for image save
        self.isVideo   = False    # model2 for video save
        self.isMonitor = False    # monittor
        self.imageCentroid = ()   # image contours centroid
        self.imageArea     = 0    # image contours area
        self.centroidDistanceLimit = 400  # more than this and alarm
        self.isFinder      = False # for person find
        self.isRecognizer  = False # for face recognize
        self.peopleNameDict = {}   # for people recognize        
        self.isAddFrame   = False  # get the condition
        self.videoName    = ''     # for video send
        self.saveFile     = '../test/timefile/'    
        self.time         = None
        self.timeList     = []
        self.isWechat     = False
        self.wechatTimeList = []
                                   
    def connectionMade(self):
        print 'Got connection from', self.transport.client
        if self.factory.number_of_connections >= self.factory.max_connections:  
            self.transport.write('Too many connections, try again later')  
            self.transport.loseConnection()  
            return      
        self.factory.number_of_connections += 1      #总连接数+1 
        self.timeout_deferred = reactor.callLater(SimpleProtocol.timeout, self.transport.loseConnection)  
    
    def connectionLost(self, reason):
    	Protocol.connectionLost(self, reason)  
        print "locst connection:",reason  
        #客户端没断开一个链接，总连接数-1  
        self.factory.number_of_connections -= 1  
        print "number_of_connections:",self.factory.number_of_connections     
        if self.outWriter:
            self.outWriter.release()
            self.isVideo = False        # release cv2 objects
        flieList = os.listdir(self.imageDir)   # delete tmp image in ../images/
        for f in flieList:
            if 'tmp' in f:
                os.remove(self.imageDir + f)
        resultDict = {}
        resultDict["normalCount"] = len(self.timeList)        
        timeArray = np.array(self.timeList)
        resultDict['normal_time'] = timeArray.mean()
        if len(self.wechatTimeList) > 0:    #在此过程中发送了微信
            resultDict["wechatCount"] = len(self.wechatTimeList)
            wechatArray = np.array(self.wechatTimeList)
            resultDict["wechat_time"] = wechatArray.mean() 
        resultJson = json.dumps(resultDict)
        fp = open(self.saveFile,'a')
        fp.write('\n')
        fp.write(resultJson)

        fp.close()

    def dataReceived(self, data):        
        if data == "model1":
            self.isImage = True
            self.saveFile = self.saveFile + 'model1.txt'
            self.dataSend('1')  
        elif data == "model2":
            self.isVideo = True              
            fourcc = cv2.cv.FOURCC(*'XVID')               # fourcc encode for video
            now = datetime.datetime.now()
            now = now.strftime('%Y%m%d-%H%M%S')          #day-hour-minute-second
            videoName = self.videoDir + 'VID' + now +'.avi'
            self.outWriter = cv2.VideoWriter(videoName,fourcc, 10.0,(640,480)) 
            self.saveFile = self.saveFile + 'model2.txt'            
            self.dataSend('1')   
        elif data == "model3":
            self.isMonitor = True
            self.saveFile = self.saveFile + 'model3.txt'
            self.dataSend('1') 
        elif data == "model4":
            self.isFinder = True  
            self.saveFile = self.saveFile + 'model4.txt'                
            self.dataSend('1')  
        elif data == 'model5':
            self.isRecognizer = True
            self.saveFile = self.saveFile + 'model5.txt'
            self.dataSend('1')
        elif data == 'start':
            self.imageFile = ''
            self.time = time.time()
        elif data == 'end': 
            if self.isImage is True:                  
                now = datetime.datetime.now()
                now = now.strftime('%Y%m%d-%H%M%S')
                filename = self.imageDir + 'IMG' + now + '.jpg'              
                imageName  = self.saveImage(self.imageFile,filename)   # save binary image
                print "save image..."                       

            elif self.isVideo is True:
                tmpImageName = self.imageDir + 'model2_tmp_image' + '.jpg'
                imageName  = self.saveImage(self.imageFile,tmpImageName)
                frame = cv2.imread(imageName)                     # read image as numpy.ndarray               
                if frame.shape[:2] != (480,640):
                    log.msg("frame size is not (240,320),cv2.resize it ")
                    frame = cv2.resize(frame,(480,640),cv2.INTER_CUBIC)            
                self.outWriter.write(frame)       # save as video file             

            elif self.isMonitor is True:
                tmpImageName = self.imageDir + 'model3_tmp_image' + '.jpg'  
                imageName  = self.saveImage(self.imageFile,tmpImageName)
                frame = cv2.imread(imageName)          
                centroidArea = imageFunction.findCentroid(frame)                
                if not self.imageCentroid:
                    self.imageCentroid = centroidArea[0]
                    self.imageArea     = centroidArea[1]                    
                else:
                    centroid,area = centroidArea[0],centroidArea[1]
                    C = (centroid[0] - self.imageCentroid[0])**2 + (centroid[1] - centroidArea[1])**2
                    centroidDistance = math.sqrt(C)
                    print "centroidDistance ----------- ",centroidDistance
                    if centroidDistance > self.centroidDistanceLimit:
                        self.isAddFrame = True
                        if not self.outWriter:
                            now = datetime.datetime.now()
                            now = now.strftime('%Y%m%d-%H%M%S') #day-hour-minute-second
                            videoName = self.videoDir + 'VIDMODEL4' + now + '.avi'
                            fourcc = cv2.cv.FOURCC(*'XVID')
                            self.outWriter = cv2.VideoWriter(videoName,fourcc, 2.0,(640,480)) 
                            self.videoName =  self.videoDir + 'VIDMODEL4' + now
                    if self.isAddFrame:
                        self.outWriter.write(frame)       # save as video file 
                        self.frameCount = self.frameCount + 1                
                    if self.frameCount > 19:                        
                        self.outWriter = None   
                        self.isAddFrame = False 
                        self.frameCount = 0                                                               
                        media_name = imageFunction.videoTransform(self.videoName)
                        media_type = 'video/mp4'
                        access_token = mychat.getTokenIntime()
                        up_load_dict = mychat.media_upload(access_token,media_name,media_type)  # type(up_load_dict) = dict
                        video_id = up_load_dict["media_id"]
                        video_dict = mychat.sendVideoMsg(access_token,video_id,"go2newera0006")
                        video_dict = json.loads(video_dict)
                        self.isWechat = True
                        if video_dict['errmsg'] != 'ok':
                            print "erro happens when send wechat video message:",video_dict['errmsg']                    
                        os.remove(self.videoName + '.avi')
                        os.remove(self.videoName + '.mp4')

            elif self.isFinder is True:                
                tmpImageName = self.imageDir + 'model4_tmp_image' + '.jpg'
                imageName  = self.saveImage(self.imageFile,tmpImageName)
                frame = cv2.imread(imageName)                     # read image as numpy.ndarray               
                if frame.shape[:2] != (480,640):
                    log.msg("frame size is not (240,320),cv2.resize it ")
                    frame = cv2.resize(frame,(480,640),cv2.INTER_CUBIC)         
                cascadeClassfier.prepareImage(frame)
                cascadeClassfier.findUpperbody()
                bodyNumber = cascadeClassfier.upperbodyNumber
                if bodyNumber > 0:
                    self.isAddFrame = True
                    if not self.outWriter:
                        now = datetime.datetime.now()
                        now = now.strftime('%Y%m%d-%H%M%S') #day-hour-minute-second
                        videoName = self.videoDir + 'VIDMODEL4' + now + '.avi'
                        fourcc = cv2.cv.FOURCC(*'XVID')
                        self.outWriter = cv2.VideoWriter(videoName,fourcc, 2.0,(640,480)) 
                        self.videoName =  self.videoDir + 'VIDMODEL4' + now      
                if self.isAddFrame:
                    self.outWriter.write(frame)       # save as video file 
                    self.frameCount = self.frameCount + 1                
                if self.frameCount > 19:
                    # self.outWriter.release()
                    self.outWriter = None   
                    self.isAddFrame = False 
                    self.frameCount = 0                                                               
                    media_name = imageFunction.videoTransform(self.videoName)
                    media_type = 'video/mp4'
                    access_token = mychat.getTokenIntime()
                    up_load_dict = mychat.media_upload(access_token,media_name,media_type)  # type(up_load_dict) = dict
                    video_id = up_load_dict["media_id"]
                    video_dict = mychat.sendVideoMsg(access_token,video_id,"go2newera0006")
                    video_dict = json.loads(video_dict)
                    self.isWechat = True
                    if video_dict['errmsg'] != 'ok':
                        print "erro happens when send wechat video message:",video_dict['errmsg']                    
                    os.remove(self.videoName + '.avi')
                    os.remove(self.videoName + '.mp4')                    
                print "bodyNumber -------------- ",bodyNumber

            elif self.isRecognizer is True:
                tmpImageName = self.imageDir + 'model5_tmp_image' + '.jpg'
                imageName  = self.saveImage(self.imageFile,tmpImageName)
                image  = cv2.imread(imageName)  # read image as numpy.ndarray
                faceResult = getFaceToPredict(image)    # return "flag","face"
                faceFlag = faceResult["flag"]             
                if faceFlag is True:
                    face = faceResult["face"]                 
                    recognizeResult = faceRecognizer.facePredict(face)                    
                    label = recognizeResult["label"]                                   
                    if str(label) in labelsDict:
                        peopleName = labelsDict[str(label)] 
                        print 'I have recognized the person is ---------- %s' % (peopleName,)
                        access_token = mychat.getTokenIntime()    # wechat alarming
                        message = 'I have recognized the person is ---------- %s' % (peopleName,)
                        txt_dict = mychat.sendTxtMsg(access_token,message,'go2newera0006')
                        txt_dict = json.loads(txt_dict)     #{u'errcode': 0, u'errmsg': u'ok'} 
                        if txt_dict['errmsg'] != 'ok':
                            log.msg('erro hapens in model5 when send text message after face recognize')
                        image_type = "image/jpg"
                        image_name = '../images/model5_tmp_image.jpg'
                        image_upload_dict = mychat.media_upload(access_token,image_name,image_type)
                        image_id = image_upload_dict["media_id"]   
                        image_dict = mychat.sendImageMsg(access_token,image_id,"go2newera0006")
                        image_dict = json.loads(image_dict)    #{u'errcode': 0, u'errmsg': u'ok'}        
                        self.isWechat = True
                        if image_dict['errmsg'] != 'ok':
                            log.msg('erro hapens in model5 when send image message after recognize it!')
                        
            else:
                pass        
            if self.isWechat:
                self.wechatTimeList.append(time.time() - self.time)
                self.isWechat = False              
            else:
                self.timeList.append(time.time() - self.time)              
            self.dataSend('1')
        else:
            self.imageFile = self.imageFile + data
          
           
    def dataSend(self,data):
        if data is None:
            log.mes("you put no data in dataSend to %s") %self.transport.client
            return
        else:
            self.transport.write(data)

    def loseConnection(self):
        self.transport.loseConnection()

    '''
    def makeConnection(self,):
        pass            
    '''

    def saveImage(self,data,filename):  
        try:
            fp = open(filename,'wb')
            fp.write(data)
            fp.close()
            self.hasImage = True
            return filename
        except Exception,ex:
            print "open file erro:",ex
            return None

# 实例化Factory  
class TimerFactory(Factory):  
    protocol = SimpleProtocol  
    #最大链接数  
    max_connections = 10       # maxmuim of clients at one time
    monitorCentroid = 500      # lager than this and warming
    monirorMinArea  = 200      # lager than this and warming
  
    def __init__(self):  
        self.number_of_connections = 0  

factory = TimerFactory()
# 监听指定的端口
# log.startLogging(open('./xmlfile/logs.txt','a'))
log.startLogging(sys.stdout)
reactor.listenTCP(1314, factory)
# 开始运行主程序
reactor.run()
