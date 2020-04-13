# reddityouranytone

This is a tool to fetch DMR ID database, convert it to Anytone D868/D878 CPS format and add known redditor u/names to the list so that this info is on the radio screen. It may work also on B-Tech DMR-6x2.

This tool is written in python and requires pandas

TODO: keep city or state data from DB when reddit data is incomplete.

Usage:
```
$ ./reddityouranytone.py

RedditYourAnytone: A tool for downloading the current DMR database and reddit ham list
and combining for upload to Anytone DMR HTs by vk3dan

fetching DMR database file (~9MB)
fetching reddit hams csv file (<1MB)

reformatting DMR database to suit Anytone...
finding redditors and updating info, this may take a while

output.csv created with 159142 entries
$
```
