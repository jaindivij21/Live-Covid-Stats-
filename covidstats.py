# program to show the covid stats

# api = https://api.covid19india.org/districts_daily.json
import ssl
import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import matplotlib.pyplot as plt

# establish sql connection
conn = sqlite3.connect("geodata.sqlite")
cur = conn.cursor()

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://api.covid19india.org/districts_daily.json'

# reads the entire webpage as a string through read function
print("")
print('Retrieving Information...')

string = urllib.request.urlopen(url, context=ctx).read()
js = json.loads(string)


def visuals():
    width_in_inches = 35
    height_in_inches = 15
    dots_per_inch = 100
    plt.figure(figsize=(width_in_inches, height_in_inches),dpi=dots_per_inch)

    dateLst = []
    activeCasesLst = []
    confirmedCasesLst = []
    deceasedCasesLst = []
    recoveredCasesLst = []
    cur.execute('SELECT id FROM Districts WHERE district = ? ', (cityName,))
    cityId = cur.fetchone()[0]
    cur.execute('SELECT state_id FROM Districts WHERE district = ? ', (cityName,))
    stateId = cur.fetchone()[0]
    cur.execute('SELECT state FROM States WHERE id = ? ', (stateId,))
    stateName = cur.fetchone()[0]

    reqdLst = js["districtsDaily"][stateName][cityName]
    for item in reqdLst:
        date1 = item["date"] # 2020-07-12
        date1 = date1[6:]
        date1 = date1.replace("-","/")
        dateLst.append(date1)
        activeCasesLst.append(item["active"])
        confirmedCasesLst.append(item["confirmed"])
        deceasedCasesLst.append(item["deceased"])
        recoveredCasesLst.append(item["recovered"])

    plt.plot(dateLst, activeCasesLst, label="Active Cases")
    plt.plot(dateLst, confirmedCasesLst, label="Confirmed Cases")
    plt.plot(dateLst, deceasedCasesLst, label="Deceased Cases")
    plt.plot(dateLst, recoveredCasesLst, label="Recovered Cases")
    plt.xlabel('Date')
    # naming the y axis
    plt.ylabel('Cases')
    # giving a title to my graph
    plt.title('Covid Stats')
    # show a legend on the plot
    plt.legend()
    # function to show the plot
    plt.show()


# ask for the city/district name
cityName = input("Enter the district name for information? ")

askForVisuals = int(
    input("Do You request for 1) Visualization of Stats or 2) Just the Numbers for this District? (1/2) "))
if askForVisuals == 1:
    visuals()
    exit()
else:
    pass

dateOfInfo = input("Enter the date of stats? (YYYY-MM-DD) ")

cur.execute('SELECT id FROM Districts WHERE district = ? ', (cityName,))
cityId = cur.fetchone()[0]
cur.execute('SELECT state_id FROM Districts WHERE district = ? ', (cityName,))
stateId = cur.fetchone()[0]
cur.execute('SELECT state FROM States WHERE id = ? ', (stateId,))
stateName = cur.fetchone()[0]

reqdLst = js["districtsDaily"][stateName][cityName]
for item in reqdLst:
    if item["date"] == dateOfInfo:
        activeCases = item["active"]
        confirmedCases = item["confirmed"]
        deceasedCases = item["deceased"]
        recoveredCases = item["recovered"]
        break
    else:
        continue

cur.execute(
    '''INSERT OR IGNORE INTO Covid (city_id, active, confirmed, deceased, recovered, dates) VALUES ( ?, ?, ?, ?, ?, ? )''',
    (cityId, activeCases, confirmedCases, deceasedCases, recoveredCases, dateOfInfo))
conn.commit()

print("\nCovid Stats of", cityName, "on", dateOfInfo, "are:")
print("Active Cases:", activeCases)
print("Confirmed Cases:", confirmedCases)
print("Deceased Cases:", deceasedCases)
print("Recovered Cases:", recoveredCases)
