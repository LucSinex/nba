#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:15:01 2017

@author: luc
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

filename = '2008_09_10_midseason_3_month_team_avgs_include_fp_avg.csv'

data = pd.read_csv(filename)

#X = data[0: