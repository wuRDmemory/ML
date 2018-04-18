#!/usr/bin/env python
# coding: utf-8

# 读取一个文件的数据并进行K近临算法

import os
import re
import numpy as np
import matplotlib.pyplot as plt

# 从数据中读取数据
def read_data_from_txt(file_path):
    # 判断该路径是否存在
    if not os.path.exists(file_path):
        print file_path, 'not exists'
        return []
    else: # 文件是存在的
        file_lines = list()
        # 打开文件并读取
        with open(file_path, 'rw') as fp:
            # 读取到最后的地方
            for line in fp.readlines():
                # 去除头尾的数据
                line = line.strip()
                # 对数据进行切片
                # lines = line.split('\t')
                lines = re.split(r'[\s]', line)
                # 
                file_lines.append(lines)
        # 读取完文件之后进行返回
        return file_lines

# 将给出的数据list进行划分，划分出数据和标签
def split_data_set(data_set):
    # 数据的list
    datas = list()
    # 标签的list
    label = list()
    # 遍历所有的数据
    for data in data_set:
        # 提取出数据
        datas.append([float(data[0]), float(data[1]), float(data[2])])
        label.append(data[-1])
    # 返回数据和标签 
    return np.array(datas), label

# 把整个数据集分为训练集和测试集
def data_train_test(data, label):
    train_data = data[0:900, :]
    train_lable = label[0:900]
    test_data = data[900:, :]
    test_label = label[900:]
    return train_data, train_lable, test_data, test_label

# 对数据进行归一化
def data_normalize(datas):
    # 列表
    data_max = list()
    data_min = list()
    # 遍历所有的列
    for i in xrange(datas.shape[1]):
        # 最大最小
        _max = np.amax(datas[:,i])
        _min = np.amin(datas[:,i])
        data_max.append(_max)
        data_min.append(_min)
        
    return data_max, data_min
    
# 数据的可视化
def show_data(datum, labels, test=None):
    # 建立一个画布
    fig, axes = plt.subplots(2, 2, sharex=False, sharey=False)
    love = list()
    small_love = list()
    not_love = list()
    # 如果没有测试点
    for i in xrange(len(labels)):
        # 先区分出三个人
        if labels[i] == 'largeDoses':
            love.append(datum[i,:])
        elif labels[i] == 'smallDoses':
            small_love.append(datum[i,:])
        else:
            not_love.append(datum[i,:])
    
    love = np.array(love)
    small_love = np.array(small_love)
    not_love = np.array(not_love)
    # 数据的可视化
    axes[0,0].scatter(love[:,0], love[:,1], c = 'r', marker = '.', s=10)
    axes[0,1].scatter(love[:,1], love[:,2], c = 'r', marker = '.', s=10)
    axes[1,0].scatter(love[:,0], love[:,2], c = 'r', marker = '.', s=10)

    axes[0,0].scatter(small_love[:,0], small_love[:,1], c = 'b', marker = '.', s=10)
    axes[0,1].scatter(small_love[:,1], small_love[:,2], c = 'b', marker = '.', s=10)
    axes[1,0].scatter(small_love[:,0], small_love[:,2], c = 'b', marker = '.', s=10)

    axes[0,0].scatter(not_love[:,0], not_love[:,1], c = 'g', marker = '.', s=10)
    axes[0,1].scatter(not_love[:,1], not_love[:,2], c = 'g', marker = '.', s=10)
    axes[1,0].scatter(not_love[:,0], not_love[:,2], c = 'g', marker = '.', s=10)
    
    # if test:
    #     # 画出test数据在图中的位置
    plt.show()

# 寻找最近邻
def find_neighbor(test, datas, labels, k):
    # 把test数据变为与datas一般大小的数据
    # tile是把数组按照x方向重复a次，y方向重复b次
    np_test = np.tile(test, (datas.shape[0],1))
    # 计算差距
    diff = np_test-datas
    # 平方
    diff = np.square(diff)
    # 加和
    diff_sum = np.sum(diff, 1)
    # 对sum进行排序
    sort_idx = np.argsort(diff_sum)
    # 之后对距离最小的前k个进行总结
    rlt_dict = {'largeDoses': 0, 'smallDoses': 0, 'didntLike': 0}
    for i in range(k):
        # 得到标签
        label = labels[sort_idx[i]]
        v = rlt_dict[label]
        rlt_dict[label] = v + 1
    # 对dict进行排序
    rlt_dict = sorted(rlt_dict.items(), key=lambda x: x[1])
    # 打印出来
    # print rlt_dict[2][0]
    # 
    return rlt_dict[2][0]

def data_verify(train_data, train_label, test_data, data_max, data_min):
    if train_data.shape[1] != len(data_max):
        print 'train data的维度与归一化参数的维度不符'
        return []
    # 先把数据进行归一化
    for i in xrange(len(data_max)):
        # 归一化的分母
        coff = data_max[i] - data_min[i]
        # 归一化训练数据
        train_data[:,i] = (train_data[:,i] - data_min[i])/coff
        # 归一化测试数据
        test_data[:,i] = (test_data[:,i] - data_min[i])/coff

    # 遍历所有待测试的数据
    verify_label = list()
    for test in test_data:
        res = find_neighbor(test, train_data, train_label, 7)
        verify_label.append(res)

    # 
    return verify_label

# label的对比
def label_compare(label, ref_label):
    # 先判断维度
    if len(label) != len(ref_label):
        print 'label 之间的维度不同，请重新确认'

    # 逐个判断
    cnt = 0
    for i in xrange(len(label)):
        print label[i], ref_label[i]
        if label[i] == ref_label[i]:
            cnt = cnt + 1

    return float(cnt)/len(label)
# 主函数
if __name__ == '__main__':
    # 文件的路径
    file_path = os.path.join(os.getcwd(), 'k-lin', 'data.txt')
    # 从文件中获取数据
    data_set = read_data_from_txt(file_path)
    # print data_set
    # 判断是否有数据
    if not data_set:
        print 'Read data.txt error！'
        exit()
    
    # 划分数据，data是np的数组
    data, label = split_data_set(data_set)
    # 把数据分为训练数据集和测试数据集
    train_data, train_label, test_data, test_label = data_train_test(data, label)
    # 数据的可视化
    show_data(train_data, train_label)
    # 对每一特征的数据求最大最小值
    data_max, data_min = data_normalize(train_data)
    # 对数据集进行验证
    verify_label = data_verify(train_data, train_label, test_data, data_max, data_min)
    # label的对比
    right = label_compare(verify_label, test_label)
    # 
    print right

    
