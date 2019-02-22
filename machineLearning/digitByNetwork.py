#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/12/5
import numpy as np
import random
import mnist_loader
# 初始化
class Network(object):
    def __init__(self,size):
        self.num_layers = len(size)
        self.size = size
        self.biases = [np.random.randn(y,1) for y in size[1:]]  # 生成偏移量
        # wjk就是连接第2层中第k个神经元和第3层中第j个神经元的权重系数,
        self.weights = [np.random.randn(y,x)
                        for x,y in zip(size[:-1],size[1:])] #生成初始的连接权重值

    def feedforward(self,a):
        # 计算每一层的神经元的输出值，将a′=σ(wa+b) 应用到每一层神经元上
        for b,w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self,training_data, epochs, mini_batch_size, eta,test_data=None):
        # 实现随机梯度下降算法,epochs:训练代数，eta:学习率η，mini_batch_size:
        if test_data:n_test = len(test_data)
        n = len(training_data)
        for j in xrange(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in xrange(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print 'Eprch {0}: {1} / {2}'.format(
                    j, self.evaluate(test_data), n_test
                )
            else:
                print 'Epoch {0} complete'.format(j)
    def update_mini_batch(self, mini_batch, eta):
        # 更新网络的权重和偏移量通过梯度下降使用反向传播,mini_batch是一个元素是元组的list，
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b,delta_nabla_w = self.backprop(x,y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x]  # list to store all the activations, layer by layer
        zs = []  # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
                sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]

        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations - y)
def sigmoid(z):
    # 如果输入的是一个向量或者Numpy数组，Numpy自动地对向量的每一个元运用sigmoid函数
    return 1.0/(1.0+np.exp(-z))
def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))


def main():
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
    net = Network([784,30,10])
    net.SGD(training_data,30,10,3.0,test_data=test_data)
if __name__ == '__main__':
    main()