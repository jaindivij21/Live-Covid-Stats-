# Program to fetch data about Covid stats and visualize them through a graph

import ssl
import urllib.request, urllib.parse, urllib.error
import json
import sqlite3

print(
    "\n-------------------------------------------- Welcome To CovidStats --------------------------------------------\n")

# establish sql connection
conn = sqlite3.connect("geodata.sqlite")
cur = conn.cursor()

# schema for india's geodata
cur.executescript('''
    CREATE TABLE IF NOT EXISTS States (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        state TEXT NOT NULL UNIQUE,
        type INTEGER NOT NULL         
    );
    
    CREATE TABLE IF NOT EXISTS Districts (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        district TEXT NOT NULL,
        state_id INTEGER NOT NULL,
        FOREIGN KEY (state_id) REFERENCES States (id)         
    );
    
    CREATE TABLE IF NOT EXISTS Covid (
        city_id INTEGER NOT NULL UNIQUE,
        active INTEGER,
        confirmed INTEGER,
        deceased INTEGER,
        recovered INTEGER,
        dates DATE,
        FOREIGN KEY (city_id) REFERENCES Districts (id)         
    );
''')

databaseUpdate = input("Do you want to update the National Geographic Database? (Y/N)")
if databaseUpdate == 'yes' or databaseUpdate == 'y' or databaseUpdate == 'Y' or databaseUpdate == 'ya':
    import geostats

import covidstats
