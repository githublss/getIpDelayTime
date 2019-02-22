#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/11/21
# the kaggle first program by KNN
import numpy as np
import pandas as pd
import csv
import operator
import datetime

def getTrainLabelAndMat():
    # 读取tain.csv文件
    traincsv = pd.read_csv(r'C:/Users/123/Desktop/kaggle/digit/train.csv')
    # 取出label
    trainLabel = traincsv.values[0:,:1]
    # 取出训练数据
    trainMat = traincsv.values[0:,1:]
    trainMat[trainMat>0] = 1

    return trainLabel, trainMat

def getTestMat():
    testcsv = pd.read_csv(r'C:/Users/123/Desktop/kaggle/digit/test.csv')
    testMat = testcsv.values
    testMat[testMat>0] = 1
    # 返回测试矩阵
    return testMat

# 分类函数，输入当前向量、训练矩阵，矩阵中向量对应标签，k值大小，返回类别
def classifyDigit(nowVect, dataSet, labels, k):
    # 得到训练矩阵行数
    dataSetSize = dataSet.shape[0]
    # 做差，平方，按行相加，开根
    diffMat = np.tile(nowVect, (dataSetSize, 1)) - dataSet  #np.tile的作用是将nowVect重复行dataSetSize次，列重复1次。为了生成一个与dataSet大小相同的矩阵
    sqDiffMat = diffMat ** 2
    sqDistance = sqDiffMat.sum(axis=1)  # 按行相加，axis=0按列相加
    distances = sqDistance ** 0.5
    # 根据距离排序
    # sortedDistIndicies = distances.argsort()
    sortedDistIndicies = np.argsort(distances) # argsort得到的是distances的从小到大排序后，在原数组中对应的索引号
    # 统计前k近的点中各个类别的数量
    classCount = {}
    for i in range(k):
        nowlabel = str(labels[sortedDistIndicies[i]])   # 找到距离训练集中按距离排序，前k个标签
        print type(nowlabel)
        classCount[nowlabel] = classCount.get(nowlabel, 0) + 1
    # 迭代一遍找到出现次数最多的类别
    maxCount = 0
    answer = ""
    for k, v in classCount.iteritems():
        if v > maxCount:
            maxCount = v
            answer = k
    return answer

def check(k):
    trainLabel,trainMat = getTrainLabelAndMat()
    testMat = getTestMat()
    # 存储结果
    testLabel = []
    testId = range(1,testMat.shape[0] + 1)
    cnt = 0
    for nowVect in testMat:
        nowLabel = classifyDigit(nowVect,trainMat,trainLabel,k)
        print type(nowLabel)
        testLabel.append(int(nowLabel[1]))
        cnt += 1
        print cnt,int(nowLabel[1])
    dataframe = pd.DataFrame({'ImageId':testId, 'Label':testLabel})
    dataframe.to_csv(r'C:/Users/123/Desktop/kaggle/digit/submission2.csv',index=False)

if __name__ == '__main__':
    start = datetime.datetime.now()
    check(3)
    end = datetime.datetime.now()
    print '花费时间：'+ str(end - start)