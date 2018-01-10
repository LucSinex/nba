#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 22:56:46 2017

@author: luc
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

create_data = False

if create_data:
    data = pd.read_csv('2008_09_10_midseason_1_month_avg_include_fp_avg_with_ids.csv',
                       delimiter=' ')
    player_list = np.unique(data.player.tolist())
    def calculate_overall_averages(data, player_list):
        d = dict()
        
        for pl in player_list:
            d[pl] = np.mean(data.loc[data.player==pl].as_matrix()[:, 4:], axis=0)[-1]
        
        return d
    pl_avgs = calculate_overall_averages(data, player_list)

players =  list(pl_avgs.keys())
values = list(pl_avgs.values())
sort_index = np.argsort(values).tolist()
sort_index.reverse()
players = [players[ind] for ind in sort_index]
values = [values[ind] for ind in sort_index]

player_count = len(players)

fig, ax = plt.subplots(1,1)
num_to_show = 15
labels = players[0:num_to_show]
ax.set_xticks(range(num_to_show))
ax.set_xticklabels(labels, rotation='vertical', fontsize=10)
plt.bar(range(num_to_show), values[0:num_to_show])
fig.show()