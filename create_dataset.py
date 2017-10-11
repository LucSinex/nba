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

client = MongoClient()
db = client.nba
games = db.games_curated

prev_months_avgd = 1

begin_date = datetime.datetime(2008, 12, 15)
end_date = datetime.datetime(2009, 3, 15)

stats_used_arr = ['ast', 'blk', 'drb', 'fg', 'fg3', 'fg3_pct', 'fg3a', 
                  'fg_pct', 'fga', 'ft', 'ft_pct', 'fta', 'mp', 'orb', 
                  'pf', 'pts', 'stl', 'tov', 'trb']

g = games.find({"date": {"$gte": begin_date, "$lt": end_date}}).next()


print (g['date'])
print (g['_id'])
game_stats = stat_functions.game_stats(games, g)

with open('test.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(stats_used_arr)
    
    for team in game_stats:
        team_tot = game_stats[team]['team_tot']
        
        for player in game_stats[team]['players']:
            player_stats = game_stats[team]['players'][player]
            
            row = []
            for field in stats_used_arr:
#                row.append(player_stats['recent_avg'][field] / team_tot[field])
                row.append(field)
            row.append(player_stats['fp'])
            
            writer.writerow(row)
    
#for team in game_stats:
#    for player in game_stats[team]:
        
print (game_stats)
    