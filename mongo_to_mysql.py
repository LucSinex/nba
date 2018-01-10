#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 17:34:27 2017

@author: luc
"""

import mysql.connector
from pymongo import MongoClient

cnx = mysql.connector.connect(user='root', password='M!ch3ls0n',
                              host='127.0.0.1',
                              database='nba_games')
cursor = cnx.cursor()

# create STATS table
stat_fields = ['ast', 'blk', 'drb', 'fg', 'fg3', 'fg3_pct', 'fg3a', 'fg_pct', 
 'fga', 'ft', 'ft_pct', 'fta', 'mp', 'orb', 'pf', 'player', 'team' , 'pts', 
 'stl', 'tov', 'trb']
create_table_sql = "create table stats (game_id int, "
for ind, f in enumerate(stat_fields):
    if (f == 'player' or f == 'team'):
        create_table_sql += f + " varchar(255)"
    else:
        create_table_sql += f + " float"
    
    if ind < len(stat_fields) - 1:
     create_table_sql += ", "
create_table_sql += ');'
print(create_table_sql) 
#cursor.execute(create_table_sql)

# create GAME_INFO table
game_info_fields = ['game_id', 'date', 'home', 'home_abbrev', 'home_score', 'away', 'away_abbrev', 'away_score']
create_game_info = "create table game_info (game_id int, date date, home varchar(255), home_abbrev varchar(255), home_score int, away varchar(255), away_abbrev varchar(255), away_score int, home_won boolean, away_won boolean)"
print(create_game_info)
#cursor.execute(create_game_info)

# Create Mongo connection
client = MongoClient()
db = client.nba
games = db.games_curated

def insert_player_data(cursor, ind, team_name, player_data):
    for p in player_data:
        stats_table_row = []
        for s in stat_fields:
            if (s == 'team'):
                stats_table_row.append(team_name)
            stats_table_row.append(p[s])
        add_row = ("INSERT INTO stats "
               "(ast, blk, drb, fg, fg3, fg3_pct, fg3a, fg_pct, fga, ft,"
               "ft_pct, fta, mp, orb, pf, player, pts, stl, tov, trb)"
               "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,"
               "%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)")
        row_data = tuple(stats_table_row)
        
        cursor.execute(add_row, row_data)

def insert_team_data(cursor, ind, teams):
    for t in teams:
        game_id = ind
        
            
        
ind = 0
for g in games.find():
    teams = g['teams']
    players_0 = g['box'][0]['players']
    players_1 = g['box'][1]['players']
    team_0 = g['box'][0]['team']
    team_0_name = teams[0]['name']
    team_1 = g['box'][1]['team']
    team_1_name = teams[1]['name']
    
    insert_player_data(cursor, ind, team_0_name, players_0)
    insert_player_data(cursor, ind, team_1_name, players_1)
    
#    insert_team_data(cursor, ind, teams
#    insert_player_data(cursor, ind, {})
    
    ind += 1
    
cnx.close()