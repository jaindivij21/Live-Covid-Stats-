# PROGRAM TO INSERT STATES AND DISTRICTS INTO THE geostats.sqlite

import ssl
import urllib.request, urllib.parse, urllib.error
import json
import sqlite3

# establish sql connection
conn = sqlite3.connect("geodata.sqlite")
cur = conn.cursor()

# open the file state_district.json
fname = "state_district.json"
string = open(fname).read()
# data is a dictionary of all the data
data = json.loads(string)

for i in range(0, 37):
    nameOfState = (data["states"][i]["name"])
    if data["states"][i]["type"] == "Union Territory":
        typeOf = 0
    else:
        typeOf = 1

    # inserting states and UTs into the states table
    cur.execute('''INSERT OR IGNORE INTO States (state, type) VALUES ( ?, ? )''', (nameOfState, typeOf))
    cur.execute('SELECT id FROM States WHERE state = ? ', (nameOfState,))
    statename_id = cur.fetchone()[0]

    # inserting districts into districts table
    districtLst = data["states"][i]["districts"]
    for item in districtLst:
        cityName = (item["name"])
        cur.execute('''INSERT OR IGNORE INTO Districts (district, state_id) VALUES ( ?, ? )''',
                    (cityName, statename_id))

    # commit
    conn.commit()