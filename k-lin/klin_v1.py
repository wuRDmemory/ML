#!/usr/bin/env python
# coding: utf-8

import numpy as np

# 产生数据
def create_data_set():
    group = np.array([[1,100],[5,89],[100,10],[105,8]])
    labs = ['love', 'love', 'action', 'action']
    return group, labs

# 对数据进行分类
def classify(dst_data, src_data, src_labs, k):
    # 先把要分类的数据写成和数据集维度一致的数组
    array_dst_data = np.tile(dst_data, [len(src_data), 1])
    # 之后对两个矩阵进行相减操作
    diff = array_dst_data - src_data
    # 进行平方操作
    square_diff = diff**2
    # 计算每个列的和
    squara_dis = square_diff.sum(1)
    # 计算开方
    dis = np.sqrt(squara_dis)
    # 对距离进行排序，注意这里是索引
    dis_with_order = np.argsort(dis, axis=0)
    # 使用词典进行记录
    map_dict = dict()
    for label in src_labs:
        map_dict[label] = 0
    # 得到K紧邻
    for i in range(k):
        map_dict[src_labs[dis_with_order[i]]] = map_dict[src_labs[dis_with_order[i]]]+1
    # 获取哪一个是最大的
    max = 0
    lab = ''
    for k, v in map_dict.items():
        if(v > max):
            max = v
            lab = k
    # 打印结果
    print lab
    
    

if __name__=='__main__':
    # 数据
    group, labs = create_data_set()
    # 测试数据
    test_data = np.array([1,1])
    # 计算
    classify(test_data, group, labs, 3)