# DALEK
---
Shodan query thingy at this point.


## Requirements
---
* >= Python 3.5.1  
* Recommend pip....

### Python Modules
---
* shodan
* requests
* json

## INSTALLATION
---
```
pip install -r requirements.txt
```

## Usage
---
```
$ python dalek.py --help
usage: dalek.py [-h] [--api_key API_KEY] [--kill-time KILL_TIME]
                [--increment INCREMENT] [--file FILE] [--keyword KEYWORD]
                [--all_results] [--alert-manager]
                [--find-exploit FIND_EXPLOIT]

A shodan scraper looking for botnets utilizing and exploiting vulnerable and
misconfigured docker.socket instances

optional arguments:
  -h, --help            show this help message and exit
  --api_key API_KEY     Api key from api.shodan.io goes here
  --kill-time KILL_TIME
                        How long you want the program to scan
  --increment INCREMENT
                        How far increments of scans will be in hours.
                        (Example: 1, 2, 3)
  --file FILE           File with all shodan api query strings
  --keyword KEYWORD     Single query string to search shodan with
  --all_results         Get larger amount of results. Usage: --all_results
                        --keyword or --all_results --file <path> (!! WARNING:
                        This will use up a large number of query credits !!)

Monitor:
  Set up alerts for monitoring ips from scans.

  --alert-manager       Semi gui input thing for creating alerts

Exploits:
  Query Exploits from Shodans Exploit API

  --find-exploit FIND_EXPLOIT
                        Find Exploits Based off keyword search

```
