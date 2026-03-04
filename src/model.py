#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Machine Learning Model Module
机器学习模型模块

This module defines model classes for traffic congestion prediction,
supporting multiple ML algorithms including Decision Tree, Random Forest,
GBRT, and more.

本模块定义了用于交通拥堵预测的模型类，
支持多种机器学习算法，包括决策树、随机森林、GBRT等。

Supported Python: 3.8+
"""

import os
import numpy as np
import pickle as pk




class model_v1(object):
    '''
    模型，
       
    训练：用到dataset类，dataset类继承sample类
    推断：用到sample类，只取inputs的key值
    存储：
    读取:
    评估：
    '''
 
    def __init__(self):
        self.data_dict = {
            'model' : -9999,  #机器学习/深度学习 算法模型
            'model_name' : -9999,
            'info' : {},
                }
        
        self.keys_list = ['model', 'model_name', 'info']
        
        
    def printdict(self):
        '''
        打印数据
        '''
        for key in self.keys_list:
            print(key, self.data_dict[key])
            
        print('\n')
        return True
    
    
    def load_information(self, info_data):
        '''
        数据信息录入
        '''
        self.data_dict['model_name'] = info_data.data_dict['model_name']
        self.data_dict['info'] = info_data.data_dict['info']
        return True

    def savepkl(self, file_path:str):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file = open(file_path,'wb')
            pk.dump(self.data_dict, file)
            file.close()
            return True
        except Exception as e:
            print("!!! save pkl file %s with Error: %s" % (file_path, e))
            return False

    def loadpkl(self, file_path:str):

        file = open(file_path,'rb')
        data_dict_load = pk.load(file)
        for key in self.keys_list:
            self.data_dict[key] = data_dict_load[key]
            
        file.close()
        return True
    



import sklearn.ensemble as ske
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn import tree
from sklearn import ensemble
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import ExtraTreeRegressor

class Model_MachineLearning(object):
   '''
   模型，
   
   读取:
   
   训练：
   
   存储：
   
   评估：计算均方根差rmse
   '''
 
   def __init__(self):
        # self.model = ske.RandomForestRegressor(n_estimators=100)
        # self.model = LinearRegression()
        # self.model = KNeighborsRegressor(n_neighbors=3)
        # self.model = SVR()
        self.model = tree.DecisionTreeRegressor()
        # self.model = ensemble.AdaBoostRegressor(n_estimators=50)#这里使用50个决策树
        # self.model = ensemble.GradientBoostingRegressor(n_estimators=100)#这里使用100个决策树
        # self.model = BaggingRegressor()
        # self.model = ExtraTreeRegressor()
   def predict(self, inputs:np.array):
       
       y_predict = self.model.predict(inputs)
       
       return y_predict
   
       # y_outputs_dict = {}
       # y_outputs_dict['outputs'] = y_predict 
       # y_outputs_dict['info'] = 'outputs'
       
       # return y_outputs_dict

   def train(self, data_set_inputs:np.array, data_set_labels:np.array):
       '''
       模型训练：

       '''
       
       self.model.fit(data_set_inputs, data_set_labels) 
       return True


   def save_model(self, file_path:str):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file = open(file_path,'wb')
            pk.dump(self.model, file)
            file.close()
            return True
        except Exception as e:
            print("!!! save pkl file %s with Error: %s" % (file_path, e))
            return False


   def load_model(self, file_path:str):
        try:
            file = open(file_path,'rb')
            model_load = pk.load(file)
            self.model = model_load
            file.close()
            return True
        except Exception as e:
            print("!!! load pkl file %s with Error: %s" % (file_path, e))
            return False
   

   def rmse(self, y_predict, y_actual):
       
       Y_predict = y_predict.reshape([-1,1])
       Y_actual = y_actual.reshape([-1,1])
       N = Y_actual.shape[0]
       
       error = Y_actual - Y_predict
       
       rmse = np.sqrt(np.dot(error.T,error)/N)
       return rmse[0][0]
   
    
   def score(self, x_test, y_test):
       
       return  self.model.score(x_test, y_test)
   


if __name__ == '__main__':
    #测试一下
    pass
