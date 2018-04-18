#!/usr/bin/env python
# coding: utf-8


import os
import math
import numpy as np
import matplotlib.pyplot as plt

# generate data
def generate_data():
    dataSet = [[0, 0, 0, 0, 'no'],         #数据集
            [0, 0, 0, 1, 'no'],
            [0, 1, 0, 1, 'yes'],
            [0, 1, 1, 0, 'yes'],
            [0, 0, 0, 0, 'no'],
            [1, 0, 0, 0, 'no'],
            [1, 0, 0, 1, 'no'],
            [1, 1, 1, 1, 'yes'],
            [1, 0, 1, 2, 'yes'],
            [1, 0, 1, 2, 'yes'],
            [2, 0, 1, 2, 'yes'],
            [2, 0, 1, 1, 'yes'],
            [2, 1, 0, 1, 'yes'],
            [2, 1, 0, 2, 'yes'],
            [2, 0, 0, 0, 'no']]
    labels = ['年龄', '有工作', '有自己的房子', '信贷情况']        #分类属性
    return dataSet, labels                #返回数据集和分类属性

# split data by yes or no
def split_data_yes_no(data):
    yes = [x for x in data if x[4]=='yes']
    no = [x for x in data if x[4]=='no']
    return yes, no

# 对第col列进行分割
def classify_by_colume(datum, col):
    dic = dict()
    for data in datum:
        if data[col] in dic:
            lis = dic[data[col]]
            lis.append(data)
        else:
            dic[data[col]] = [data,]
    return dic

# calculate shannon entropy
def calc_shannon_ent(**argv):
    # use dict to map the kind and its value
    # class sum
    class_sum = 0
    # each class's cnt
    classes = list()
    for key in argv:
        classes.append(float(len(argv[key])))
    # each class appears percentile
    # classes = classes/sum(classes)
    class_sum = sum(classes)
    # calcu each kind's percentile
    # calc each kind's information
    infos = list()
    for i in range(len(classes)):
        classes[i] = classes[i]/class_sum
        if classes[i] == 0:
            infos.append(0)
        else:
            infos.append(classes[i]*math.log(classes[i],2))
    # calcu entropy
    entropy = sum(infos)
    # return 
    return -entropy

def create_tree(datum, indexes, labels, depth):
    if len(indexes) == depth:
        return 'no' 
    gross_number = len(datum)
    print datum
    # distinguish
    yes_data, no_data = split_data_yes_no(datum)
    # calculate the gross entropy
    dic = {'kind1':yes_data, 'kind2':no_data}
    gross_ent = calc_shannon_ent(**dic)
    max_idx = 0
    max_ent = 0
    max_datum = list()
    # 对特征进行分类
    for i in range(len(labels)):
        if i in indexes:
            continue
        # i represent colume
        cla = classify_by_colume(datum, i)
        cla_condition_ent = 0
        for k,v in cla.items():
            percentile = float(len(v))/gross_number
            yes, no = split_data_yes_no(v)
            dic = {'kind1':yes, 'kind2':no}
            perc_ent = calc_shannon_ent(**dic)
            cla_condition_ent += percentile*perc_ent
        if (gross_ent-cla_condition_ent) > max_ent:
            max_ent = gross_ent-cla_condition_ent
            max_idx = i
            yes, no = split_data_yes_no(datum)
            max_datum = no
    indexes.append(max_idx)
    next_depth = create_tree(max_datum, indexes, labels, depth)
    tem = {1: 'yes', 0: next_depth}
    return {labels[max_idx]: tem}
        
# main function
if __name__=='__main__':
    # generate data
    datum, labels = generate_data()
    # gross_number = len(datum)
    # # distinguish
    # yes_data, no_data = split_data_yes_no(datum)
    # # calculate the gross entropy
    # dic = {'kind1':yes_data, 'kind2':no_data}
    # gross_ent = calc_shannon_ent(**dic)
    # max_idx = 0
    # max_ent = 0
    # max_
    # # 对特征进行分类
    # for i in range(len(labels)):
    #     # i represent colume
    #     # 对第i列进行分类
    #     cla = classify_by_colume(datum, i)
    #     cla_condition_ent = 0
    #     for k,v in cla.items():
    #         percentile = float(len(v))/gross_number
    #         yes, no = split_data_yes_no(v)
    #         dic = {'kind1':yes, 'kind2':no}
    #         perc_ent = calc_shannon_ent(**dic)
    #         cla_condition_ent += percentile*perc_ent
    #     if gross_ent-cla_condition_ent > max_ent:
    #         max_ent = gross_ent-cla_condition_en
    #         max_idx = i
    indexes = []
    tree = create_tree(datum, indexes, labels, 2)
    for k,v in tree.items():
        print k, v

    