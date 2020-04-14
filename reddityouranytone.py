#!/usr/bin/env python

import csv
import urllib2
import os.path
import time
import pandas as pd

dbfile = "user.csv"
redditfile = "nicks.csv"
outputfile = "output.csv"
current_time = time.time()
dburl = "https://www.radioid.net/static/user.csv"
redditurl = "https://raw.githubusercontent.com/molo1134/qrmbot/master/lib/nicks.csv"

print ("\nRedditYourAnytone: A tool for downloading the current DMR database and reddit ham list\nand combining for upload to Anytone DMR HTs by vk3dan\n")

if os.path.isfile(outputfile):
    os.unlink(outputfile)

# get the current database csv from radioid.net
if os.path.isfile(dbfile):
    print("user.csv found")
    creation_time = os.path.getctime(dbfile)
    if (current_time - creation_time) // (24 * 3600) >= 7:
        print("file over 7 days old, fetching current version (~9MB)")
        os.unlink(dbfile)
        response = urllib2.urlopen(dburl)
        with open(dbfile, 'w') as f: f.write(response.read ())
    else:
        print("user.csv current")
else:
    print("fetching DMR database file (~9MB)")
    response = urllib2.urlopen(dburl)
    with open(dbfile, 'w') as f: f.write(response.read ())

# get the current reddit hams csv from molo1134's github

if os.path.isfile(redditfile):
    print("nicks.csv found")
    creation_time = os.path.getctime(redditfile)
    if (current_time - creation_time) // (24 * 3600) >= 28:
        print("file over 28 days old, fetching current version (<1MB)\n")
        os.unlink(redditfile)
        response = urllib2.urlopen(redditurl)
        with open(redditfile, 'w') as f: f.write(response.read ())
    else:
        print("nicks.csv current\n")
else:
    print("fetching reddit hams csv file (<1MB)\n")
    response = urllib2.urlopen(redditurl)
    with open(redditfile, 'w') as f: f.write(response.read())

# manipulate DMR csv to suit anytone
print("reformatting DMR database to suit Anytone...")
df = pd.read_csv(dbfile, dtype=object)
df.drop([0], axis=0, inplace=True)
df.insert(0,"No.",df.index.T)
df.insert(9,"Call Type","Private Call")
df.insert(10,"Call Alert","None")
df.drop(["LAST_NAME", "REMARKS"], axis=1, inplace=True)
df.insert(7,"Remarks","")
df = df.rename(columns={"RADIO_ID": "Radio ID", "CALLSIGN": "Callsign", "FIRST_NAME": "Name", "CITY": "City", "STATE": "State", "COUNTRY": "Country"})

# do the reddit limbo
rf = open(redditfile, 'r')
csv_rf = csv.reader(rf)
print ("finding redditors and updating info, this may take a while\n")
for row in csv_rf:
    if row[1] and row[2]:
        df.loc[df["Callsign"] == row[0], ["City", "State"]] = "IRC: "+row[1], row[2]
    else: 
        if row[1]:
            df.loc[df["Callsign"] == row[0], ["City"]] = "IRC: "+row[1]
        else:
            if row[2]:
                df.loc[df["Callsign"] == row[0], ["State"]] = row[2]
df.to_csv(outputfile, index=False)
print("output.csv created with "+repr(df.index.size)+" entries")