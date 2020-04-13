#!/usr/bin/env python

import csv
import urllib2
import os.path
import pandas as pd

dbfile = "user.csv"
redditfile = "nicks.csv"
workingfile = "working.csv"
outputfile = "output.csv"

print ("\nRedditYourAnytone: A tool for downloading the current DMR database and reddit ham list\nand combining for upload to Anytone DMR HTs by vk3dan\n")

# get the current database csv from radioid.net
if os.path.isfile(dbfile):
    print("user.csv found, moving on")
else:
    print("fetching DMR database file")
    dburl = "https://www.radioid.net/static/user.csv"
    response = urllib2.urlopen(dburl)
    with open(dbfile, 'w') as f: f.write (response.read ())

# get the current reddit hams csv from molo1134's github

if os.path.isfile(redditfile):
    print("nicks.csv found, moving on\n")
else:
    print("fetching reddit hams csv file\n")
    redditurl = "https://raw.githubusercontent.com/molo1134/qrmbot/master/lib/nicks.csv"
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
df.to_csv(workingfile, index=False)
print (repr(df.index.size)+ " DMR IDs output to working.csv")

# reopen working file and reddit file
wf = open(workingfile, 'r')
csv_wf = csv.reader(wf)
rf = open(redditfile, 'r')
csv_rf = csv.reader(rf)
for row in csv_wf:
    datawf=[row[2],row[4],row[5]]
    for row in csv_rf:
        if row[0]==datawf[0]:
            print(row[0]) # this doesn't work
# i don't know wtf to do from here to match callsigns in dmr id to the ones in nicks.csv
# still to do: the above, and copy irc nicks over City if applicable, and reddit u/names over state, if applicable.
