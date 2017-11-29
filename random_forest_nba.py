#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 22:13:44 2017

@author: luc
"""
#from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
#from sklearn.preprocessing import StandardScaler
#from sklearn.model_selection import train_test_split
#from sklearn import metrics
#from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
import numpy as np

filename = '2008_09_10_midseason_1_month_avg_include_fp_avg_rounded.csv'

data = pd.read_csv(filename, delimiter=' ')
data_as_m = data.as_matrix()
X = data_as_m[:, 0:20]
y = data_as_m[:, 20:]
#train, test = train_test_split(data, test_size=0.2)
#
#d_train = train.as_matrix()
#X_train = d_train[:, 0:160]
#y_train = d_train[:, 160]
#
##forest = RandomForestRegressor()
##regr = MultiOutputRegressor(forest)
#regr = MLPRegressor(hidden_layer_sizes=(80, 40, 40),max_iter=1000)
#regr.fit(X_train, y_train)
#
#d_test = test.as_matrix()
#X_test = d_test[:, 0:160]
#y_test = d_test[:, 160]

kf = KFold(n_splits=5)
scaler = StandardScaler()

results = {}

for L1 in range (30, 40, 10):
    for L2 in range(20,25,5):
        for L3 in range(10, 11):
            layer_sizes_str = "L1: " + str(L1) + ", L2: " + str(L2) + ", L3: " + str(L3)
            print(layer_sizes_str)
            model = MLPRegressor(hidden_layer_sizes=(L1,L2,L3),max_iter=1000)
            
            scores = []
            for train_index, test_index in kf.split(X):
                #    print("TRAIN:", train_index, "TEST:", test_index)
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
            
                scaler.fit(X_train)  # Don't cheat - fit only on training data
                X_train = scaler.transform(X_train)
                X_test = scaler.transform(X_test)  # apply same transformation to test data
                
                model.fit(X_train, y_train)
                
                y_predict = model.predict(X_test)
            #    for i in range(20):
            #        print("Prediction: " + str(y_predict[i]))
            #        print("Actual :" + str(y_test[i]))
                score = model.score(X_test, y_test)
                
#                print("Score: " + str(score))
#                print("--------------------")
                
                scores.append(score)
            results[layer_sizes_str] = scores

for size in results:
    print(size + ": " + str(np.mean(results[size])))

#score = regr.score(X_test, y_test)
#print("Accuracy: %f" % score)