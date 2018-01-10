#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:23:07 2017

@author: luc
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold

# Constants
NUM_CLUSTERS = 5
MAX_ITER = 5000

# Load Data
#data = pd.read_csv('2008_09_10_midseason_1_month_avg_include_fp_avg_rounded.csv',
#                   delimiter=' ')
data = pd.read_csv('2008_09_10_midseason_1_month_avg_include_fp_avg_with_ids.csv',
                   delimiter=' ')
with_ids = True

# Find last index of data for separation later
if (with_ids):
    end_index = data.shape[1] - 4
    d_vals = [arr[3:].tolist() for arr in data.values]
else:
    end_index = data.shape[1] - 1
    d_vals = data.values

# Create Kmeans clusterer and standardscaler
km = KMeans(n_clusters=NUM_CLUSTERS)
scaler = StandardScaler()

# Permute data and divide into X and y
permuted_data = np.random.permutation(d_vals)
m = len(permuted_data)
X_all = permuted_data[:, 0:end_index]
y_all = permuted_data[:, end_index]

# Separate X into km, train, and test sets
X_km = X_all[0:(int(np.ceil(m*0.1)))]
X_train = X_all[int(np.ceil(m*0.1)):int(np.ceil(m*0.8))]
X_test = X_all[int(np.ceil(m*0.8)):m]
# now y
y_train = y_all[int(np.ceil(m*0.1)):int(np.ceil(m*0.8))] #.reshape((-1,1))
y_test = y_all[int(np.ceil(m*0.8)):m] #.reshape((-1,1))

# Fit scaler to all training data, X_km included
scaler.fit(np.concatenate((X_train, X_km)))
X_km = scaler.transform(X_km)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Fit KMeans to the X_km set
# Later used to separate X_train into clusters to perform regression on
km.fit(X_km)

# Layer sizes
base_sizes = (24, 16, 4)
layer_sizes = base_sizes
ensemble_layer_sizes = base_sizes

# TRAINING
# Divide data by k-means and create a model on each cluster
model_dict = dict()
for i in range(NUM_CLUSTERS):
    cl = 'cluster_' + str(i)
    model_dict[cl] = dict()
    
    # Identify which cluster to send training data to
    model_dict[cl]['X_train'] = X_train[km.predict(X_train) == i]
    model_dict[cl]['y_train'] = y_train[km.predict(X_train) == i]
    
    # Create model and save it in dict
    tmpmodel= MLPRegressor(hidden_layer_sizes=ensemble_layer_sizes, max_iter=MAX_ITER)
    tmpX_train = model_dict[cl]['X_train']
    tmpy_train = model_dict[cl]['y_train']
    tmpmodel.fit(tmpX_train, tmpy_train)
    model_dict[cl]['model'] = tmpmodel

# TESTING
def ensemble_predict(sample):
    return model_dict['cluster_' + str(km.predict(sample)[0])]['model'].predict(sample)
#    return np.mean([model_dict['cluster_' + str(i)]['model'].predict(sample) for i in range(NUM_CLUSTERS)])

ensemble_predictions = [ensemble_predict(x.reshape(1,-1)) for x in X_test]
ensemble_predictions = np.squeeze(ensemble_predictions)

def rmse(predictions, real):
    error_arr = list()        
    for idx, prd in enumerate(predictions):
        error_arr.append(np.power(real[idx].reshape(-1,1) - prd, 2))
    rmse = np.sqrt(np.mean(error_arr))
    return rmse

print("Ensemble RMSE: " + str(rmse(ensemble_predictions, y_test)))

# Try a normal model without k-means clustering
regr = MLPRegressor(hidden_layer_sizes=(layer_sizes), max_iter=MAX_ITER)
regr.fit(X_train, y_train)
regr_preds = regr.predict(X_test)
print("Regressor RMSE: " + str(rmse(regr_preds, y_test)))






# Inspect different cluster values for fun
# Tends to get good separation for mean of y values    
#print(data.columns)
#for cluster in model_dict:
#    print(cluster)
#    print([np.mean(model_dict[cluster]['X_train'], axis=1), 
#           np.mean(model_dict[cluster]['y_train'], axis=0)])
#    
#
#n_x = 50
#pred_graph = plt.plot(predictions[0:n_x])
#real_graph = plt.plot(y_test[0:n_x])
#plt.xlabel('Player game samples')
#plt.ylabel('Fantasy Pts')
#
#plt.legend()























