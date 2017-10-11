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

begin_date = datetime.datetime(2008, 12, 16)
end_date = datetime.datetime(2009, 3, 15)

stats_used_arr = ['ast', 'blk', 'drb', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 
                  'fg3_pct', 'ft', 'fta', 'ft_pct', 'mp', 'orb', 
                  'pf', 'pts', 'stl', 'tov', 'trb']

#g = games.find({"date": {"$gte": begin_date, "$lt": end_date}}).next()
#print (g['date'])
#print (g['_id'])
#game_stats = stat_functions.game_stats(games, g)

games_examined = games.find({"date": {"$gte": begin_date, "$lt": end_date}})
games_total = games_examined.count()
print ("Games found: " + str(games_total))

filename = '2008_09_midseason_1_month_avg.csv'

try:
    os.remove(filename)
except OSError:
    print ('File does not exist')
    
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    col_names = stats_used_arr.copy()
    col_names.append('fp')
    writer.writerow(col_names)
    
    row_count = 1
    g_counter = 1
    for g in games_examined:
        print ("Processing game {} of {}".format(str(g_counter), str(games_total)))
        print ("Game id: " + str(g['_id']))
        game_stats = stat_functions.game_stats(games, g)
        
        for team in game_stats:
            team_tot = game_stats[team]['team_tot']
            
            for player in game_stats[team]['players']:
    #            print ("Writing row {}: {}".format(str(i), player))
                player_stats = game_stats[team]['players'][player]
                
                row = []
                for field in stats_used_arr:
                    row.append(player_stats['recent_avg'][field] / team_tot[field])
    #            print (str(row[0]))
                row.append(player_stats['fp'])
                
                writer.writerow(row)
                row_count += 1
        
        print ("Game complete. Totals rows in dataset: " + str(row_count))
        g_counter += 1
#for team in game_stats:
#    for player in game_stats[team]:
        
#print (game_stats)
    