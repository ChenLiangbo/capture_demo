#!usr/bin/env/python 
# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
import cv2
import numpy as np
import datetime

# 定义你Protocol类
class SimpleProtocol(Protocol):

    timeout = 1000

    def __init__(self):        
        self.hasImage = False
        self.image_file = ''                       #to store image binary stream from socket
        self.image_name = '../images/pic'          #the path saving picture
        self.image_num  = 100                      #the number of saving picture
        self.image_count = 0                       #to count picture recieve
        self.out = None                            # cv2 objects to store video
    def connectionMade(self):
        print 'Got connection from', self.transport.client
        if self.factory.number_of_connections >= self.factory.max_connections:  
            self.transport.write('Too many connections, try again later')  
            self.transport.loseConnection()  
            return  
         
        # self.transport.buffersize = 1024*1024
        self.factory.number_of_connections += 1      #总连接数+1 
        self.timeout_deferred = reactor.callLater(SimpleProtocol.timeout, self.transport.loseConnection)  
        fourcc = cv2.cv.FOURCC(*'XVID')               # fourcc encode for video
        now = datetime.datetime.now()
        now = now.strftime('%Y%m%d-%H%M%S') #day-hour-minute-second
        videoName = './video/VID' + now +'.avi'
        self.out = cv2.VideoWriter(videoName,fourcc, 20.0, (640,480)) 

    def connectionLost(self, reason):
    	Protocol.connectionLost(self, reason)  
        print "locst connection:",reason  
        #客户端没断开一个链接，总连接数-1  
        self.factory.number_of_connections -= 1  
        print "number_of_connections:",self.factory.number_of_connections  
        self.out.release()                                 # release cv2 objects
     
    def dataReceived(self, data):
        print "data recvived..."
        image_data = data
        # print "len(data) = ",len(data)
        if image_data == 'start':
            self.image_file = ''
        elif image_data == 'end':                   
            image_name       = self.save_image(self.image_file)   # save binary image
            frame = cv2.imread(image_name)                        # read image as numpy.ndarray
            self.out.write(frame)                                 # save as video file

            self.image_count = self.image_count + 1 
            self.image_count = self.image_count % self.image_num 
            print "recvive image successfully...."  

        else:
            self.image_file = self.image_file + data
            print "data = ",len(data)
            # print "len(self.image_file) = ",len(self.image_file) 
    '''
    def makeConnection(self,):
        pass      
    '''
    def save_image(self,data):
        filename = self.image_name + str(self.image_count) + '.jpg'
        print "filename = ",filename
        try:
            fp = open(filename,'w')
            fp.write(data)
            fp.close()
            self.hasImage = True
            return filename
        except Exception,ex:
            print "open file erro:",ex
            return None


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


# 实例化Factory
# 设置factory的protocol属性以便它知道使用哪个protocol与客户端通信(这就是所谓的你的自定义
# protocol)
class TimerFactory(Factory):  
    protocol = SimpleProtocol  
    #最大链接数  
    max_connections = 10  
  
    def __init__(self):  
        self.number_of_connections = 0  


factory = TimerFactory()

# 监听指定的端口
reactor.listenTCP(1314, factory)

# 开始运行主程序
reactor.run()
