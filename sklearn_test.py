#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:04:35 2017

@author: luc
"""

import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold

# import dataset
filename = '2008_09_10_midseason_1_month_avg_include_fp_avg.csv'
#filename = '2008_09_midseason_1_month_avg.csv'

data = np.genfromtxt(filename, skip_header=1, delimiter=' ')
X = data[:, 0:-1]
y = data[:, -1]

#low_scorers = y_all < 15
#select_scorers = X[:, -1] > 4
#X = X[select_scorers, :]
#y = y[select_scorers]

# Split the data into low scorers and high scorers, need to base this
# on previous fantasy points average, need to include recent fantasy point
# average in recent_avgs function

#data = {"low": {X: }}
#print(low_scorers)


# EVERYTHING BELOW HERE WORKS TO FIT DATA AND FIND R^2, WILL MODIFY BY BREAKING
# INTO low_scorers, high_scorers REGIMES TO SEE IF THIS IMPROVES FIT
# CURRENTLY R^2 is around 0.55, not good enough I think

kf = KFold(n_splits=5)
scaler = StandardScaler()

results = {}

for L1 in range (30, 40, 10):
    for L2 in range(20,25,5):
        for L3 in range(10, 11):
            layer_sizes_str = "L1: " + str(L1) + ", L2: " + str(L2) + ", L3: " + str(L3)
            print(layer_sizes_str)
            model = MLPRegressor(hidden_layer_sizes=(L1,L2,L3),max_iter=2000)
            
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