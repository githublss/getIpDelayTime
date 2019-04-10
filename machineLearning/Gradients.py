#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2019/3/23
# 使用梯度下降法，来
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib
m = 20
def main():

    x0 = np.ones((m, 1))
    x1 = np.arange(1, m+1).reshape(m, 1)
    X = np.hstack((x0, x1))     # 将两个数组中的元素拼接起来

    y = np.array([
        3, 4, 5, 5, 2, 4, 7, 8, 11, 8, 12,
        11, 13, 13, 16, 17, 18, 17, 19, 21
    ]).reshape(m, 1)

    alpha = 0.01
    optimal = gradient_descent(X ,y,alpha)
    print 'optimal:',optimal
    print 'error_function:',error_function(optimal, X, y)[0, 0]
    line1 = [(0,optimal[0]),(m,optimal[0]+optimal[1]*m)]
    (line1_xs, line1_ys) = zip(*line1)


    fig,ax = plt.subplots(figsize=(10,5))
    ax.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='blue'))
    ax.plot(x1,y,'g*')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('y with x change')
    plt.show()

def error_function(theta, X, y):
    """error function j definition.代价函数"""
    diff = np.dot(X, theta) - y
    # print diff,'**'
    return (1./2*m * np.dot(np.transpose(diff), diff))

def gradient_function(theta, X, y):
    """Gradient of the function j definition，代价函数的梯度"""
    diff = np.dot(X,theta) - y

    return (1./m) * np.dot(np.transpose(X), diff)

def gradient_descent(X, y, alpha):
    """perform gradient descent，梯度下降迭代计算"""
    theta = np.array([1, 1]).reshape(2, 1)
    gradient = gradient_function(theta, X, y)
    while not np.all(np.absolute((gradient) <= 1e-5)):
        theta = theta - alpha * gradient
        gradient = gradient_function(theta, X, y)
    return theta

if __name__ == '__main__':
    main()