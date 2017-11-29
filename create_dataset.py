#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 15:53:31 2017

@author: luc
"""

from pymongo import MongoClient
import datetime
import stat_functions
import csv
import os

client = MongoClient()
db = client.nba
games = db.games_curated

NUM_PLAYERS = 8

years = [2008, 2009]
year_dict = dict()
games_by_year = list()
for year in years:
    begin_date = datetime.datetime(year, 12, 16)
    end_date = datetime.datetime(year+1, 3, 15)
    gs = games.find({"date": {"$gte": begin_date, "$lt": end_date}})
    games_by_year.append(gs)
    print(str(year) + ': ' + str(gs.count()))
    
stats_used_arr = ['avg_fp', 'ast', 'blk', 'drb', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 
                  'fg3_pct', 'ft', 'fta', 'ft_pct', 'mp', 'orb', 
                  'pf', 'pts', 'stl', 'tov', 'trb']
  
#filename = '2008_09_10_midseason_1_month_team_avgs_include_fp_avg.csv'
#row_type = 'team'
filename = '2008_09_10_midseason_1_month_avg_include_fp_avg.csv'
row_type = 'player' 

try:
    os.remove(filename)
except OSError:
    print ('File does not exist')

def top_n_players(n, team_player_avgs):
    avgs = team_player_avgs.copy()
    top_n_players = []
    for i in range(n):
        name = max(avgs.keys(), key=(lambda key: avgs[key]['recent_avg']['avg_fp']))
        top_n_players.append(name)
        del avgs[name]
    return top_n_players

def recent_avgs_to_example(team_player_avgs, stats_used_arr):
    num_players = NUM_PLAYERS
    num_p_on_team = len(team_player_avgs.keys())
    
    if num_p_on_team < num_players:
        print ("Not enough players")
        return None
    else:
        i = 0
        row = []
        fp_row = []
        for player in top_n_players(num_players, team_player_avgs):
            for stat in stats_used_arr:
                row.append(team_player_avgs[player]['recent_avg'][stat])
            fp_row.append(team_player_avgs[player]['fp'])
            i += 1
            if i == num_players:
                row = row + fp_row
                return row
    
    
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    col_names = stats_used_arr.copy()
    if row_type == 'player':
        col_names.append('fp')
        writer.writerow(col_names)
    else:
        # repeat the col names for each player
        features = list()
        fp_header = list()
        for i in range(NUM_PLAYERS):
            player_features = [col + '_p' + str(i+1) for col in col_names]
            features = features + player_features
            fp_header.append('fp' + '_' + str(i+1))
        features = features + fp_header
        writer.writerow(features)
    
    row_count = 1
    g_counter = 1
    low_player_count = 0
    for games_examined in games_by_year:
        games_total = games_examined.count()
        print ("Games found: " + str(games_total))
        for g in games_examined:
            print ("Processing game {} of {}".format(str(g_counter), str(games_total)))
            print ("Game id: " + str(g['_id']))
            game_stats = stat_functions.game_stats(games, g)
            
            for team in game_stats:
                team_tot = game_stats[team]['team_tot']
                
                if (row_type == "player"):
                    for player in game_stats[team]['players']:
            #            print ("Writing row {}: {}".format(str(i), player))
                        player_stats = game_stats[team]['players'][player]
                        
                        row = []
                        for field in stats_used_arr:
                            val = player_stats['recent_avg'][field]
                            team_val = team_tot[field]
                            
                            if (field == 'avg_fp'):
                                row.append(val)
                            else:
                                row.append(val / team_val)
            #            print (str(row[0]))
                        row.append(player_stats['fp'])
                        
                        writer.writerow(row)
                        row_count += 1
                else:
                    team_player_avgs = game_stats[team]['players']
    #                print(team_player_avgs)
                    row = recent_avgs_to_example(team_player_avgs, stats_used_arr)
                    if type(row) == list:
                        writer.writerow(row)
                        row_count += 1
                    else:
                        low_player_count += 1
            print ("Game complete. Totals rows in dataset: " + str(row_count))
            g_counter += 1
#for team in game_stats:
#    for player in game_stats[team]:
        
#print (game_stats)
    