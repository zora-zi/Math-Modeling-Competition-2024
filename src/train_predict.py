#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Model Training and Prediction Module
模型训练与预测模块

This script trains machine learning models on processed traffic data
and evaluates prediction performance for different time horizons.

本脚本使用处理后的交通数据训练机器学习模型，
并评估不同时间跨度的预测性能。

"""


import os
import pandas as pd
import numpy as np

import datetime

import pickle as pk


 
def load_file(file_path: str):
    '''
    #读取字典数据
    '''
    try:
        file = open(file_path,'rb')
        data_dict_load = pk.load(file)
        file.close()
        return data_dict_load
    except Exception as e:
        print("!!! save mat file %s with Error: %s" % (file_path, e))
        return False

def save_file(file_path: str, data: dict):
    '''
    #存储字典数据
    '''
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file = open(file_path,'wb')
        pk.dump(data, file)
        file.close()
        return True
    except Exception as e:
        print("!!! save mat file %s with Error: %s" % (file_path, e))
        return False


#==========================================================================================

# Data folder path / 数据文件夹路径
folder_path = '../data'
path_dict = os.path.join(folder_path, 'processed', 'data_sets.pkl')  # Dataset path / 数据集路径

data_sets = load_file(path_dict)

data_set_names = ['data_set_5',
'data_set_10',
'data_set_15',
'data_set_20',
'data_set_25',
'data_set_30',]

models_names = ['model_5',
'model_10',
'model_15',
'model_20',
'model_25',
'model_30',]


import model
# Initialize model container / 初始化模型容器
models = model.model_v1()
models.data_dict['model_name'] = 'models_dict'
models.data_dict['info'] = {'data_set_names':data_set_names,'models_names':models_names,}

models.data_dict['model'] = {} #把所有模型存到该字典中

score2_list = []

for k in range(6):
    
    data_set_inputs = data_sets[data_set_names[k]]['inputs_train']
    data_set_labels = data_sets[data_set_names[k]]['labels_train'][:,1]
    
    model_ML = model.Model_MachineLearning()
    model_ML.train(data_set_inputs, data_set_labels)  # Train model / 模型训练
    score2 = model_ML.score(data_set_inputs, data_set_labels)
    score2_list.append(score2)
    models.data_dict['model'][models_names[k]] = model_ML 
    


# path_models = os.path.join("./data/", 'step2', 'models_dict.pkl') # 模型存储路径
# models.savepkl(path_models)


#=================================================================================


outputs_list = []
abs_error_list = []
labels_list = []
relative_error_list = []
score_list = []
for k in range(6):
    model_ML = models.data_dict['model'][models_names[k]] #载入模型


    inputs_test = data_sets[data_set_names[k]]['inputs_test'] #载入数据
    labels_test = data_sets[data_set_names[k]]['labels_test'][:,1]

    outputs = model_ML.predict(inputs_test)
    
    score1 = model_ML.score(inputs_test, labels_test)

    abs_error = abs(outputs - labels_test)
    
    relative_error = abs((outputs - labels_test)/labels_test)
    
    score_list.append(score1)
    labels_list.append(labels_test)
    outputs_list.append(outputs)
    abs_error_list.append(abs_error)
    relative_error_list.append(relative_error)

#=================================================================================      
head_list = ['time_after_5min','after_10min','after_15min','after_20min','after_25min','after_30min',]

import xlwt
book = xlwt.Workbook(encoding="utf-8")
 
# 添加一个sheet页
sheet1 = book.add_sheet('labels')
# 将列表数据写入sheet页
for i, col in enumerate(head_list):
    sheet1.write(0, i, col)
for i, row in enumerate(labels_list):
    for j, col in enumerate(row):
        sheet1.write(j+1, i, col)
        
        
# 添加一个sheet页
sheet2 = book.add_sheet('outputs')
# 将列表数据写入sheet页
for i, col in enumerate(head_list):
    sheet2.write(0, i, col)
for i, row in enumerate(outputs_list):
    for j, col in enumerate(row):
        sheet2.write(j+1, i, col)


# 添加一个sheet页
sheet3 = book.add_sheet('abs_error')
# 将列表数据写入sheet页
for i, col in enumerate(head_list):
    sheet3.write(0, i, col)
for i, row in enumerate(abs_error_list):
    for j, col in enumerate(row):
        sheet3.write(j+1, i, col)

# 添加一个sheet页
sheet4 = book.add_sheet('relatives_error')
# 将列表数据写入sheet页
for i, col in enumerate(head_list):
    sheet4.write(0, i, col)
for i, row in enumerate(relative_error_list):
    for j, col in enumerate(row):
        sheet4.write(j+1, i, col)

# 添加一个sheet页
sheet4 = book.add_sheet('score_list')
# 将列表数据写入sheet页
for i, col in enumerate(head_list):
    sheet4.write(0, i, col)
for i, col in enumerate(score_list):
    sheet4.write(1, i, col)

path_book = os.path.join('../results', 'prediction_results.xls')  # Results path / 结果存储路径
# Save results / 保存结果
os.makedirs(os.path.dirname(path_book), exist_ok=True)
book.save(path_book)

