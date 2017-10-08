#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 22:41:25 2017

@author: luc
"""

from pymongo import MongoClient
import datetime
import stat_functions

client = MongoClient()
db = client.nba
games = db.games_curated

begin_date = datetime.datetime(2009, 8, 1)
end_date = datetime.datetime(2010, 4, 1)

test_games = games.find({"date": {"$gte": begin_date, "$lt": end_date}})
print (test_games.count())

g = games.find_one()
print (g)

pipeline2 = [
        {'$match': {"date": {"$gte": begin_date, "$lt": end_date}}},
        { '$unwind': '$box' },
        { '$unwind': "$box.players" },
        { '$match': {'box.players.player': 'Ray Allen'}}
#        { '$group': {
#                '_id': None,
#                'ast': {'$avg': 'box.players.ast'},
#                'blk': {'$avg': 'box.players.blk'}}}
]

avg = stat_functions.find_recent_avg(games, 'Ray Allen', datetime.datetime(2012, 12, 25))
print (avg)

#game1 = games.aggregate(pipeline).next()
#game2 = games.aggregate(pipeline2).next()
#print (game1)
#print (game2)

#game = db.games.find_one()
#print (game.keys())
#print (game["box"][0].keys())
#print (game["box"][1].keys())
#print ("Stats: " + str(game["box"][0]["players"][0].keys()))
#for player in game["box"][0]["players"]:
#    print ("Name: " + str(player["player"]))
##for player in game["box"]:
#    
#
##for year in range(1988, 2014):
#    
#    begin_date = datetime.datetime(year, 10, 1)
#    end_date = datetime.datetime(year+1, 7, 1)
#    
#    yearly_games = games.find({"date": {"$gte": begin_date, "$lt": end_date}})
#    
#    print ("Year: " + str(year))
#    print ("Games: " + str(yearly_games.count()))