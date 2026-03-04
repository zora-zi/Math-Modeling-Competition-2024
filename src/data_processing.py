#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Data Processing Module for Highway Emergency Lane Activation Model
高速公路应急车道启用模型 - 数据处理模块

This script processes traffic monitoring data from surveillance cameras
and prepares machine learning datasets for congestion prediction.

本脚本处理来自监控摄像头的交通数据，
并为拥堵预测准备机器学习数据集。

Input: CSV files containing traffic parameters extracted from video analysis
Output: Processed datasets saved as .pkl files

"""
from datetime import datetime, timedelta

import os
import numpy as np
import pandas as pd
import datetime
import xlrd
import pickle as pk

def time2sec(y):
    '''
    时间类型时分秒转换成秒
    '''
    h = y.hour  #直接用datetime.time模块内置的方法，得到时、分、秒
    m = y.minute
    s = y.second
    return int(h)*3600 + int(m)*60 + int(s) #int()函数转换成整数运算

def sec2time(y):
    # 将秒转换为时间格式
    time = str(timedelta(seconds=y))
    return time

def read_data(file_path,flag=0):
    file_names = os.listdir(file_path)# 获取文件夹中所有文件名
    if flag == 1:
        files = [file for file in file_names if 'far' in file and file.endswith('.csv')]# 过滤出名字含'cover_far'的文件
    else:
        files = [file for file in file_names if 'uncover' in file and file.endswith('.csv')]# 过滤出名字含'uncover'的文件
    #全部初始数据存放
    raw_data = []
    data_list = []
    # 读取每个CSV文件并打印
    last_file = '1'
    for file in files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, header=None, index_col=False)
        if file[0] != last_file:
            merged_df = pd.concat(raw_data, ignore_index=True)
            data_list.append(merged_df)
            raw_data.clear()
            last_file = file[0]
        raw_data.append(df)
    merged_df = pd.concat(raw_data, ignore_index=True)
    data_list.append(merged_df)
    return data_list
 

def make_data_set(input,output,time):
    pre_time = 30#提前预警时间
    input = input.iloc[pre_time-time:-time,:]
    input.reset_index(drop=True, inplace=True)
    data = pd.concat([input,output.iloc[:,-2:]],axis=1)
    data = data.astype(float)

    data = np.array(data)
    
    
    # 获取 data 的行数
    num_rows = data.shape[0]
    # 随机挑选出 100 行的索引
    random_indices = np.random.choice(num_rows, 100, replace=False)
    # 创建一个新的 numpy 数组，包含前 50 行和后 50 行
    data_train = data[random_indices]

    
    # 随机挑选出 30 行的索引
    random_indices = np.random.choice(num_rows, 30, replace=False)
    # 使用随机索引从 data_test 中挑选出 30 行
    data_test = data[random_indices]
   
    
    
    inputs = data[:,:-2]
    labels = data[:,-2:]
    
    inputs_train = data_train[:,:-2]
    labels_train = data_train[:,-2:]
    inputs_test = data_test[:,:-2]
    labels_test = data_test[:,-2:]
    
    return inputs, labels, inputs_train, labels_train, inputs_test, labels_test

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


#=========================================================================================
# Main execution / 主程序
if __name__ == '__main__':
    # Video start time offsets (seconds) / 各视频起始秒数偏移
    time_of_video = [75, 64, 81]
    pre_time = 30  # Early warning time (minutes) / 提前预警时间（分钟）
    
    # Data folder path / 数据文件夹路径
    folder_path = '../data'
    data_list = read_data(folder_path, 0)

#数据预处理
#把每个摄像头合并后的数据秒数更新，
for data in data_list:
    num_rows = len(data)
    data.iloc[:, 0] = range(1, num_rows + 1)

#视频长度
max_time = data_list[3].shape[0]

#提取第4个摄像头数据
output = data_list.pop()
#并且将时间截取到摄像头4开始的前半小时,时长保持和摄像头4相同,后合并
for i in range(len(data_list)):
    data = data_list[i]
    print(time_of_video[i],time_of_video[i]-pre_time,max_time + time_of_video[i])
    data = data.iloc[time_of_video[i]-pre_time:(max_time + time_of_video[i]),1:] #截取到摄像头4开始的前半小时,时长保持和摄像头4相同
    data.reset_index(drop=True, inplace=True)
    data_list[i] = data
input = pd.concat(data_list, axis=1)


#生成套数据集, 存为字典型数据
inputs, labels, inputs_train, labels_train, inputs_test, labels_test = make_data_set(input,output, time=5) #跨度为5分钟（用第一个点预测第四个点）
data_set_5 = {'inputs': inputs, 'labels': labels, 'inputs_train': inputs_train, 'labels_train': labels_train, 'inputs_test': inputs_test, 'labels_test': labels_test,}

inputs, labels, inputs_train, labels_train, inputs_test, labels_test = make_data_set(input,output, time=10) #跨度为10分钟（用第一个点预测第四个点）
data_set_10 = {'inputs': inputs, 'labels': labels, 'inputs_train': inputs_train, 'labels_train': labels_train, 'inputs_test': inputs_test, 'labels_test': labels_test,}

inputs, labels, inputs_train, labels_train, inputs_test, labels_test = make_data_set(input,output, time=15) #跨度为15分钟（用第一个点预测第四个点）
data_set_15 = {'inputs': inputs, 'labels': labels, 'inputs_train': inputs_train, 'labels_train': labels_train, 'inputs_test': inputs_test, 'labels_test': labels_test,}

inputs, labels, inputs_train, labels_train, inputs_test, labels_test = make_data_set(input,output, time=20) #跨度为4分钟（用第一个点预测第四个点）
data_set_20 = {'inputs': inputs, 'labels': labels, 'inputs_train': inputs_train, 'labels_train': labels_train, 'inputs_test': inputs_test, 'labels_test': labels_test,}

inputs, labels, inputs_train, labels_train, inputs_test, labels_test = make_data_set(input,output, time=25) #跨度为4分钟（用第一个点预测第四个点）
data_set_25 = {'inputs': inputs, 'labels': labels, 'inputs_train': inputs_train, 'labels_train': labels_train, 'inputs_test': inputs_test, 'labels_test': labels_test,}

inputs, labels, inputs_train, labels_train, inputs_test, labels_test = make_data_set(input,output, time=30) #跨度为4分钟（用第一个点预测第四个点）
data_set_30 = {'inputs': inputs, 'labels': labels, 'inputs_train': inputs_train, 'labels_train': labels_train, 'inputs_test': inputs_test, 'labels_test': labels_test,}


data_sets = {
'data_set_5': data_set_5,
'data_set_10': data_set_10,
'data_set_15': data_set_15,
'data_set_20': data_set_20,
'data_set_25': data_set_25,
'data_set_30': data_set_30,
    }


path_dict = os.path.join(folder_path, 'step1', 'data_sets.pkl') # 数据集存储路径

save_file(path_dict, data_sets) #存储dict数据, 到path_dict 路径