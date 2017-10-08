#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 15:53:31 2017

@author: luc
"""

from pymongo import MongoClient
import datetime
import stat_functions

client = MongoClient()
db = client.nba
games = db.games_curated

prev_months_avgd = 1

begin_date = datetime.datetime(2008, 12, 15)
end_date = datetime.datetime(2009, 3, 15)

g = games.find({"date": {"$gte": begin_date, "$lt": end_date}}).next()


print (g['date'])
print (g['_id'])
game_stats = stat_functions.game_stats(games, g)
print (game_stats)
    