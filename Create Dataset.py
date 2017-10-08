#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 15:53:31 2017

@author: luc
"""

from pymongo import MongoClient
import datetime

client = MongoClient()
db = client.nba
games = db.games

begin_date = datetime.datetime(2011, 12, 15)
end_date = datetime.datetime(2012, 3, 1)

data = games.find({"date": {"$gte": begin_date, "$lt": end_date}})
print (data.count())