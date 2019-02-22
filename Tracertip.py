#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/10/9
import os,time
import xlrd,xlwt
import re
import numpy as np
import logging
import portalocker
from multiprocessing import process,Pool,Lock
from xlutils.copy import copy
from time import sleep
# ip 纬度 经度
def fileDeal():
    path = "finalData/"  # 要批量处理的文件夹
    files = allFile(path)  # 得到文件夹下的所有文件名称
    try:
        targetFile = xlwt.Workbook()
        targetSheet = targetFile.add_sheet('iptime')
    except Exception, e:
        print e
    j = 0
    for file in files:
        filePath = path + file
        data = xlrd.open_workbook(filePath)
        table = data.sheet_by_index(0)
        L = 6 + j
        targetSheet.write(0, L, file[:14])  # 获得创建时间
        try:
            for i in range(table.nrows):
                if j == 0:          # 将ip和地址写入，只写一次
                    for k in range(5):
                        targetSheet.write(i + 1, k, table.cell_value(i, k))
                time = table.cell_value(i, 6)
                targetSheet.write(i + 1, L, time)
        except Exception as e:
            print e, '-----------'
        j = j + 1
        print file, '======================================'
    mkdir(path+'target/')
    targetFile.save(path+'target/target.xls')  # 生成文件的目录

def allDir(path = "result/"):     # 文件夹目录，遍历所有文件夹
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        if os.path.isdir(path+file):  # 判断是否是文件夹，是文件夹才打开
            s.append(file)
    return s

def allFile(path = "result/"):     # 文件夹目录,遍历所有文件，
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(path+file):  # 判断是否是文件夹，不是文件夹才打开
            s.append(file)
    return s

def mergeFile():
    path = r"result/"  # 要批量处理的文件夹
    mkdir('finalData/')
    alldir = allDir()
    alldir = sorted(alldir, key=lambda x: os.path.getctime(os.path.join(path, x)))    # 根据文件夹的创建时间排序
    print alldir
    for everyDir in alldir:
        j=0 # 标志位，用来拷贝ip和地址
        path_files = path + everyDir
        files = os.listdir(path_files)  # 得到文件夹下的所有文件名称
        filemt = time.localtime(os.stat(path_files+'/'+files[-1]).st_mtime)     # 通过txt文件的创建时间，读取每个文件夹的时间
        fileName = time.strftime("%m-%d-%H-%M-%S", filemt)   # 合成要生成的文件的名称
        try:
            targetFile = xlwt.Workbook()
            targetSheet = targetFile.add_sheet('iptime')
        except Exception, e:
            print e
        # files = sorted(files, key=lambda x:int(filter(str.isdigit,x)))

        for file in files[:-1]:
            filePath = path_files + '/' + file
            print filePath
            data = xlrd.open_workbook(filePath)
            table = data.sheet_by_index(0)
            for i in range(table.nrows):
                if j == 0:
                    for k in range(5):
                        targetSheet.write(i, k, table.cell_value(i, k))
                if(table.cell_value(i,6)):
                    targetSheet.write(i,6,table.cell_value(i,6))
            j = 1
        saveFileName = fileName+'.xls'
        print saveFileName
        targetFile.save('finalData/'+saveFileName)

        # print fileName

def mkdir(path):    # 创建一个文件夹
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print "---  new folder...  ---"
        print "---  OK  ---"

    else:
        print "---  There is this folder!  ---"
def averagenum(num):    # 计算一个数组的平均值
    nsum = 0
    if len(num)==0:
        return 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e),'----'
def localIp(target):
    target = str(target)
    output = os.popen("curl ifconfig.me")
    myIp = output.read()  # 获取本地公网ip
    print 'publicIp:' + myIp
    mkdir('result\\result'+target)
    with open('result\\result'+target+'\\myPublicIp.txt', 'w') as f:
        f.write("本地公网IP是：{0}".format(myIp))

def write_excel(file='result\\time.xls', startIndex=0, endIndex=2,target=0):
    target = str(target)
    time = []
    total = endIndex - startIndex
    if not os.path.exists(file):
        print '请添加一个iptest.xlsx文件！！！'.decode('utf-8').encode('gbk')
        sleep(9)
    tables = excel_table_byname(file)
    count = 0
    while(count < total):
            for row in tables[startIndex:endIndex]:
                try:
                    temptime = []    # 先定义一个临时时间
                    status = 0  # 状态指示码，指示是否请求成功
                    ipStart = row[0].split('.') # 获取到ip开始段
                    ipStart = map(int, ipStart) # 将string转化为int
                    startInt = ipStart[-1]
                    ipEnd = row[1].split('.')   # 获取到ip结束段
                    ipEnd = map(int,ipEnd)      # 将string转化为int
                    endInt = ipEnd[-1]
                    requestIp = ipStart[:3]
                    requestCount = 1  # 记录请求的次数
                    requestIp.append(np.random.randint(startInt,endInt+1))  #在ip的开始段和结束段之间随机生成一个ip
                    requestIp = ".".join(map(str,requestIp))    # 组合出来一个新的真实请求ip

                    print ipEnd,ipStart,requestIp
                    sql = 'ping ' + requestIp
                    print count+startIndex, '/', startIndex ,'-',endIndex, ':', sql,os.getpid()
                    output = os.popen(sql)
                    a = output.read()
                    print a
                    if ('平均 ='.decode('utf-8').encode('gbk') not in a):  # 编码问题很烦人
                        status = 0
                    else:
                        temp = re.findall(r'\d+ms', a)  # 将ping命令的返回值中的所有时间值获取到
                        temp = str(temp[-1])
                        status = 1
                    # 判断是否有参数的返回
                    if status == 1:
                        # isInt = int(re.search(r'\d+', temp).group())
                        temptime.append(int(re.findall(r'\d+', temp)[0]))  # 将ping命令的返回值中的平均时间记录下来
                        print temptime[-1]  # 打印最后一条的信息

                    while(requestCount < 6 & (endInt-startInt) >= 1):   #判断是否进行请求的发送,如果请求没有超过三次且ip段长度大于一个才发送
                        requestIp = ipStart[:3]
                        requestIp.append(np.random.randint(startInt, endInt + 1))  # 在ip的开始段和结束段之间随机生成一个ip
                        requestIp = ".".join(map(str, requestIp))  # 组合出来一个新的真实请求ip
                        sql = 'ping ' + requestIp
                        print count+startIndex, '/', startIndex ,'-',endIndex, ':', sql,os.getpid()
                        requestCount += 1
                        output = os.popen(sql)
                        a = output.read()
                        print a

                        if ('平均 ='.decode('utf-8').encode('gbk') not in a): # 编码问题很烦人
                            status = 0
                        else:
                            temp = re.findall(r'\d+ms', a)  # 将ping命令的返回值中的所有时间值获取到
                            temp = str(temp[-1])
                            status = 1
                        # 判断是否有参数的返回
                        if status==1:
                            temptime.append(int(re.findall(r'\d+', temp)[0]))  # 将ping命令的返回值中的平均时间记录下来
                            print temptime[-1]  # 打印最后一条的信息
                    time.append(averagenum(temptime))
                    count = count +1
                except Exception as e:
                    logging.error(e)
                    time.append(0)
                    count = count + 1
                    print e

                if (count%3) == 0:

                    try:
                        data = open_excel(file)
                        # portalocker.lock(data, portalocker.LOCK_EX)
                        rows = data.sheets()[0].nrows
                        excel = copy(data)  # 将copy方法将xlrd的对象转化为xlwt的对象
                        # portalocker.lock(excel,portalocker.LOCK_EX)
                        table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
                        everyWrite = 3 # 每次写的行数

                        for i in range(everyWrite):
                            table.write(i+(count-everyWrite)+startIndex, 6, time[i+(count-everyWrite)])  # 参数分别是 行 列 值
                        excel.save('result\\result'+target+'\\'+str(startIndex)+'time.xls')
                        print '=============================================='
                        # portalocker.unlock(excel)
                        # portalocker.unlock(data)
                    except Exception as e:
                        print e,'===='

    #数据写
    data = open_excel(file)
    # rows = data.sheets()[0].nrows
    excel = copy(data)                      # 将copy方法将xlrd的对象转化为xlwt的对象
    # portalocker.lock(excel,portalocker.LOCK_EX)
    table = excel.get_sheet(0)              # 用xlwt对象的方法获得要操作的sheet
    for i in range(endIndex-startIndex):
        table.write(i+startIndex,6,time[i]) # 参数分别是 行 列 值
    excel.save('result\\result'+target+'\\'+str(startIndex)+'time.xls')
    # portalocker.unlock(excel)
def excel_table_byname(file , colnameindex=0, by_name=u'Sheet1'):
    data = open_excel(file)                 # 打开excel文件
    table = data.sheet_by_name(by_name)     # 根据sheet名字来获取excel中的sheet
    nrows = table.nrows  # 行数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list =[]                                   #  装读取结果的序列
    for rownum in range(0, nrows):           # 遍历每一行的内容
         row = table.row_values(rownum)      # 根据行号获取行
         if row: # 如果行存在
             app = [] # 一行的内容
             for i in range(len(colnames)): # 一列列地读取行的内容
                app.append(row[i])
             list.append(app)                #装载数据
    return list

def main():
    # print '正在开始工作.....'.decode('utf-8').encode('gbk')
    # for target in range(20):
    #     localIp(target)
    #     file = 'iptest.xls'
    #     tables = excel_table_byname(file)
    #     l = Lock()
    #     processNumber = 30   #将表分成Number次，分为Nmuber+1段
    #     p = Pool(processNumber+1)     # 使用进程池
    #     i=0
    #     for i in range(processNumber):
    #         p.apply_async(write_excel, args=(file, (len(tables)/processNumber*i), (len(tables)/processNumber*(i+1)),target,))
    #         print len(tables)/processNumber*i, len(tables)/processNumber*(i+1)
    #     p.apply_async(write_excel, args=(file,len(tables)/processNumber*(i+1),len(tables),target,))
    #     print len(tables)/processNumber*(i+1),len(tables)
    #     print 'start'
    #     p.close()
    #     p.join()
    #     print 'end'
    mergeFile()
    fileDeal()
if __name__ == '__main__':
    main()