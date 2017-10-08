#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 18:32:30 2017

@author: luc
"""

from pymongo import MongoClient

client = MongoClient()
db = client.nba
games = db.games_curated

print (games.find().count())

#games.find().forEach( function (obj) { 
#        for player in obj.box.players:
#            new_mp = int(player.mp[0:2]) + int(player.mp[3:5])/60
#            player.mp = new_mp 
#        games.save(obj) })

direct_to_float_fields = ['fg_pct', 'fg3_pct', 'ft_pct']

for game in games.find():
    _id = game['_id']
    #print(game)
    
    for i in range(0,2):
        for player in game['box'][i]['players']:
            if (type(player['mp']) == str):
                if (len(player['mp']) == 5):
                    new_mp = float(player['mp'][0:2]) + float(player['mp'][3:5])/60.0
                else:
                    new_mp = float(player['mp'][0:1]) + float(player['mp'][2:4])/60.0
                player['mp'] = new_mp
            
            for f in direct_to_float_fields:
                if (type(player[f]) == str and player[f] != ''):
                    #print("FG pct: " + player['fg_pct'])
                    new_val = float(player[f])
                    player[f] = new_val
    
    games.update({'_id': _id}, {'$set': game}, upsert=False)