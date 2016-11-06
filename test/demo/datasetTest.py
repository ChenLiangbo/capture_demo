#!usr/bin/env/python 
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import numpy as np

z = {} # 存储关于每张图片对应的lable
for_pre = []  # 存储用来进行测试的图片，规则是每个人10张图，5张用来训练，5张用来测试
def normalize(X, low, high, dtype=None):
    """对数据进行正常化处理，让其处于最高和最低值之间."""
    X = np.asarray(X)
    minX, maxX = np.min(X), np.max(X)
    # normalize to [0...1].
    X = X - float(minX)
    X = X / float((maxX - minX))
    # scale to [low...high].
    X = X * (high-low)
    X = X + low
    if dtype is None:
        return np.asarray(X)
    return np.asarray(X, dtype=dtype)


def read_images(path, sz=None):
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
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    # im.shape = (112,92)
                    # resize to given size (if given)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                    if y.count(c) > 4:
                        for_pre.append({'no':c,'src':np.asarray(im, dtype=np.uint8)})
                    else:
                        #x_tmp = np.asarray(im, dtype=np.uint8)
                        #x_tmp.shape =  (112, 92)
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)
                    global z
                    z[os.path.join(subject_path, filename)] = c
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
    #type(for_pre) = list,but the item is dict({"no","src"})
    return [X,y]

def prediction(model):
    """图像预测

    参数:
        model: 就是图片训练的那个model

    数据集中每个人存储了10张图片，我把其中的5张存储到for_pre，作为训练数据。用已知的lable和预测的lable作比较，得出图片识别正确的概率
    """
    tn = 0 # 识别正确的图片数
    for item in for_pre:
        [p_label, p_confidence] = model.predict(cv2.resize(item['src'],(92,112)))
        imageUsedToPridict = cv2.resize(item['src'],(92,112))
        #type(imageUsedToPridict) = numpy.ndarray
        #imageUsedToPridict.shape =  (112, 92)       
        if p_label == item['no']:
            tn = tn+1
        else:
            print 'the answer is %d,' % item['no'],
            print "Predicted label = %d (confidence=%.2f)" % (p_label, p_confidence)

    print "总共有%d次预测，其中正确次数为%d" %(len(for_pre),tn)

if __name__ == "__main__":
    # This is where we write the images, if an output_dir is given
    # in command line:
    out_dir = './xmlfile'
    sourcePath = './faceDataset'
   

    # Now read in the image data. This must be a valid path!
    [X,y] = read_images(sourcePath, (92, 112))
    
    # print "y = ",y
 
 
    # model = cv2.createEigenFaceRecognizer()
    # model = cv2.createFisherFaceRecognizer()
    model = cv2.createLBPHFaceRecognizer()
    X1 = np.asarray(X)  #X1.shape =  (200, 112, 92)
    y1 = np.asarray(y)  #y1.shape =  (200,)

    model.train(np.asarray(X), np.asarray(y))
  
    prediction(model) # 图片预测

    # You can see the available parameters with getParams():
    print model.getParams()
    # Now let's get some data:
    # mean = model.getMat("mean")
    print out_dir + '/testModelOut.xml'
    f = open(out_dir + '/testModelOut.xml','w')
    model.save(out_dir + '/testModelOut.xml')
    # eigenvectors = model.getMat("eigenvectors")
    # # We'll save the mean, by first normalizing it:
    # mean_norm = normalize(mean, 0, 255, dtype=np.uint8)
    # mean_resized = mean_norm.reshape(X[0].shape)
    # if out_dir is None:
    #     cv2.imshow("mean", mean_resized)
    # else:
    #     cv2.imwrite("%s/mean.png" % (out_dir), mean_resized)
  
    # # print "z = ",z
    # if out_dir is None:
    #     cv2.waitKey(0)