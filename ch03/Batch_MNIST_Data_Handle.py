# 通过批处理来优化FP在MNIST Data Set中的速度
import sys, os
import numpy as np
import pickle
import time
sys.path.append(os.pardir)  # 导入父目录的文件
from dataset.mnist import load_mnist  # 加载MINIST数据集

def get_data():
    '''
    Returns
        -------
        (训练图像, 训练标签), (测试图像, 测试标签)

    flattern:设置是否将输入展开（将图像展开为一维数组， 不展开为1x28x28三维图像） True：展开， False不展开
    normalize:是否将图像正规化为0.0~1.0的值。False：图像按原来的像素保持0~255， True：正规化
    '''

    (x_trian, t_trian), (x_test, t_test) = load_mnist(flatten=True, normalize=True)
    return x_test, t_test

def init_network():
    with open("sample_weight.pkl", 'rb') as f:
        network = pickle.load(f)
    # print(network)
    return network

def sigmoid_function(x):
    return 1 / (1 + np.exp(-x))

def softmax_function(a):
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y

def work(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    B1, B2, B3 = network['b1'], network['b2'], network['b3']
    A1 = np.dot(x, W1) + B1
    Z1 = sigmoid_function(A1)

    A2 = np.dot(Z1, W2) + B2
    Z2 = sigmoid_function(A2)

    A3 = np.dot(Z2, W3) + B3
    y = softmax_function(A3)

    return y

start_time = time.time()
x, t = get_data()
network = init_network()
batch_size = 100 # 批处理的数量
accuracy_cnt = 0
for i in range(0, len(x), batch_size):
    x_batch = x[i: i + batch_size] # 每次提取batchsize个数据出来进行FP处理
    y_batch = work(network, x_batch)
    p = np.argmax(y_batch, axis = 1) # 对应矩阵的第一维，矩阵的第一维代表行，第零维代表列
    accuracy_cnt += np.sum(p == t[i: i + batch_size])

print("Accuracy: " + str(float(accuracy_cnt) / len(x)))
end_time = time.time()
print("消耗时间： ", (end_time - start_time))





