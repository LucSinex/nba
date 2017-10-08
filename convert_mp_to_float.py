#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 18:32:30 2017

@author: luc
"""

from pymongo import MongoClient
import datetime

client = MongoClient()
db = client.nba
games = db.games_copy

print (games.find().count())

#games.find().forEach( function (obj) { 
#        for player in obj.box.players:
#            new_mp = int(player.mp[0:2]) + int(player.mp[3:5])/60
#            player.mp = new_mp 
#        games.save(obj) })

for game in games.find():
    _id = game['_id']
    #print(game)
    
    for player in game['box'][0]['players']:
        if (len(player['mp']) == 5):
            new_mp = float(player['mp'][0:2]) + float(player['mp'][3:5])/60.0
        else:
            new_mp = float(player['mp'][0:1]) + float(player['mp'][2:4])/60.0
        player['mp'] = new_mp
        
    for player in game['box'][1]['players']:
        if (len(player['mp']) == 5):
            new_mp = float(player['mp'][0:2]) + float(player['mp'][3:5])/60.0
        else:
            new_mp = float(player['mp'][0:1]) + float(player['mp'][2:4])/60.0
        player['mp'] = new_mp
    
    db.games_copy.update({'_id': _id}, {'$set': game}, upsert=False)