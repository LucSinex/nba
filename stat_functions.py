#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 16:20:09 2017

@author: luc
"""

import dateutil.relativedelta
import numpy as np

stat_categories = ['ast', 'blk', 'drb', 'fg', 'fg3', 'fg3_pct', 'fg3a', 
                   'fg_pct', 'fga', 'ft', 'ft_pct', 'fta', 'mp', 'orb', 
                   'pf', 'pts', 'stl', 'tov', 'trb']

def find_recent_avg(games_db, player_name, date):
#    print("Calculating Average for: " + player_name)

    begin_date = date - dateutil.relativedelta.relativedelta(months=1)
    end_date = date - dateutil.relativedelta.relativedelta(days=1)
#    print("Dates: " + str(begin_date) + " to " + str(end_date))
    
    pipeline = [
        {'$match': {"date": {"$gte": begin_date, "$lt": end_date}}},
        { '$unwind': '$box' },
        { '$unwind': "$box.players" },
        { '$match': {'box.players.player': player_name}},
        { '$group': {
                '_id': None,
                'games_used' : { '$sum': 1 }, 
                'ast': {'$avg': '$box.players.ast'},
                'blk': {'$avg': '$box.players.blk'},
                'drb': {'$avg': '$box.players.drb'},
                'fg':  {'$avg': '$box.players.fg'},
                'fg3': {'$avg': '$box.players.fg3'},
                'fg3_pct': {'$avg': '$box.players.fg3_pct'},
                'fg3a': {'$avg': '$box.players.fg3a'},
                'fg_pct': {'$avg': '$box.players.fg_pct'},
                'fga': {'$avg': '$box.players.fga'},
                'ft': {'$avg': '$box.players.ft'},
                'ft_pct': {'$avg': '$box.players.ft_pct'},
                'fta': {'$avg': '$box.players.fta'},
                'mp': {'$avg': '$box.players.mp' },
                'orb': {'$avg': '$box.players.orb'},
                'pf': {'$avg': '$box.players.pf'},
                'pts': {'$avg': '$box.players.pts'},
                'stl': {'$avg': '$box.players.stl'},
                'tov': {'$avg': '$box.players.tov'},
                'trb': {'$avg': '$box.players.trb'}
                }}
    ]
    cursor = games_db.aggregate(pipeline)
    if (cursor.alive):
        avg = games_db.aggregate(pipeline).next()
    else:
        avg = None
        
    return avg

def calculate_fp(statline):
    s = statline
    
    stats_over_10 = (int(s['pts']>=10) + int(s['trb']>=10) + int(s['ast']>=10) +
                     int(s['blk']>=10) + int(s['stl']>=10))
    
    dbl_dbl_bool = int(stats_over_10>=2)
    trp_dbl_bool = int(stats_over_10>=3)
    
    fp = (s['ast']*1.5 + s['pts'] + s['fg3']*0.5 + s['trb']*1.25 + s['stl']*2 +
          s['blk']*2 + s['tov']*(-0.5) + dbl_dbl_bool*1.5 + trp_dbl_bool*3)
    
    return fp

def game_stats(games_db, game_dict):
    stats = {}
    game_date = game_dict['date']
    print("processing game with date: " + str(game_date))
    
    for i in range(0,2):
        key = "team_" + str(i)
        stats[key] = {'players': {}, 'team_tot': {}}
        
        for player_dict in game_dict['box'][i]['players']:
            name = player_dict['player']
#            print("Name: " + name)
            stats[key]['players'][name] = {}
            stats[key]['players'][name]['fp'] = calculate_fp(player_dict)
            stats[key]['players'][name]['recent_avg'] = find_recent_avg(games_db, name, game_date)
            
            player_recent_avg = stats[key]['players'][name]['recent_avg']
            if (player_recent_avg == None):
                stats[key]['players'].pop(name)
                print ("Player popped: " + name)
            else:
                player_recent_avg['avg_fp'] = calculate_fp(player_recent_avg)
                player_recent_avg['_id'] = 1
                if (len(stats[key]['team_tot']) == 0):
                    stats[key]['team_tot'] = player_recent_avg.copy()
                else:
                    for field in player_recent_avg:
                        stats[key]['team_tot'][field] += player_recent_avg[field]
            
    return stats

def recent_avgs_to_example(team_player_avgs, stats_used):
    tpa = team_player_avgs
    num_players = len(tpa)
    
    stats_arr = np.zeros((num_players, len(stats_used)))
    fp_today_arr = np.zeros((num_players, 1))
    
    i = 0
    for player in tpa:
        for j in range(len(stats_used)):
            stats_arr[i, j] = tpa[player]['recent_avg'][stats_used[j]]
        i+=1
        
        fp_today_arr[i, 0] = tpa[player]['fp']
    
    return stats_arr, fp_today_arr
    






























