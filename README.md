# DALEK
---
Shodan query thingy at this point.

v0.1.0 :

* Preliminary Docker reporting completed.
* Keyword searching
* Query File searching
* Getting all results from shodan parsed (Keyword Search Only.)
* Basic Alert Manager Created (Shodan's Monitor)
* Preliminary ExploitDB query options for exploits  


TODO :

* Module Base reporting
* Database
* DockerFile
* Shodan scanning.
* More to come...


## Requirements
---
* >= Python 3.5.1 (tested on 3.8 so +1 for me I guess)
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

To make it easier on myself there are a couple of `os.system` calls to `$ shodan`.

For now this only refers to the `--all_results` option.

### Windows

***Ensure your path variables for python are setup correctly***

#### Install Shodan
```
C:\Users\<username>\ > easy_install shodan
```

```
C:\Users\<username>\ > shodan init <your api key>
```


### Linux

```
$ easy_install shodan
```

```
$ shodan init <your api key>
```


### Config File Setup

Sometimes you don't want to copy your api key into the terminal...

So I made a config file.

```
$ cp dalek-config.json.example dalek-config.json
```

Open `dalek-config.json` in your perferred text editor.

Example Config:

```
{
  "api_key" : "abcdefghijklmnop123456"
}

```
Save the file and dalek should work without you having to call the `--api-key` argument.


## Usage
---
```
$ python dalek.py --help
usage: dalek.py [-h] [--api_key API_KEY] [--increment INCREMENT] [--file FILE] [--keyword KEYWORD] [--all_results] [--limit LIMIT] [--alert-manager] [--find-exploit FIND_EXPLOIT]

A shodan scraper looking for botnets utilizing and exploiting vulnerable and misconfigured docker.socket instances

optional arguments:
  -h, --help            show this help message and exit
  --api_key API_KEY     Api key from api.shodan.io goes here
  --increment INCREMENT
                        How far increments of scans will be in hours. (Example: 1, 2, 3)
  --file FILE           File with all shodan api query strings
  --keyword KEYWORD     Single query string to search shodan with
  --all_results         Get larger amount of results. Usage: --all_results --keyword or --all_results --file <path> (!! WARNING: This will use up a large number of query credits !!)
  --limit LIMIT         Get a certain number of results Usage: --all_results --limit 100 --keyword or --all_results --limit 100 --file <path> (!! WARNING: This will use up a large number of query credits !!)

Monitor:
  Set up alerts for monitoring ips from scans.

  --alert-manager       Semi gui input thing for creating alerts

Exploits:
  Query Exploits from Shodans Exploit API

  --find-exploit FIND_EXPLOIT
                        Find Exploits Based off keyword search



```


# Examples

## Query Shodan

### 1. Keyword search
  ```
  $ python dalek.py --keyword "apache"
  ```
  This will grab the first one hundred (100) hosts that 'match' the keyword query.

  Also shoutout to @424f424f for the suggestion of this feature. Made my life so much easier.

### 2. Query File search

  ```
  $ python dalek.py --file ./some-queries.txt
  ```
  This will do the same as a keyword search. The difference will be in that you can have multiple queries within a file.

  1. Example
    ```
    $ echo "apache\n docker\n mysql" > some-queries.txt
    ```

    Dalek will then query shodan's api for each of those queries.

    **Be warned however as the more queries will cost more query credits. (Documentation on Query Credits can be found in shodan's api docs).**

### 3. All Results

  Some times you may want to grab all results of a query for Dalek to parse them.
  This is where the `--all_results` and `--limit` functions come in handy.

  ***Currently only works with `--keyword` search!!!***

  1. Getting all results

    ```
    $ python dalek.py --keyword "docker" --all_results
    ```

    By default, this will grab any and all results that shodan has for your query.

    *Important*: Sometimes Shodan will not give you all of the results. This is not an issue with the project. This is just the fact that shodan is awesome and everyone knows it ;)

    **Again, keep an eye on your query credits. This will drain your credits very quickly if you give it a large number (x>1000)**

  2. Limiting bulk data

    ```
    $ python dalek.py --keyword "docker" --all_results --limit 200
    ```

    For larger queries such as RDP you probably don't want to pull all of the known devices that have port 3389 out on the external net...unless you want to...

    But this is where limit comes into play. For *research* purposes you can grab "X" number of records and have them save to a `.json` file for later viewing and parsing.

    *Foreshadowing Note*: Parsing of `-export` files will be coming in the future for offline/further analysis work. This will include `.txt` files.

## Alerts


Shodan documents the Alert API as a way to monitor ips for different 'triggers' when they scan the specific devices.

I.E. If a device is vulnerable to Heartbleed on port :443 then it will 'trigger' an alert and be logged.

These examples will go over how to create, edit, and delete these alerts in Dalek.

### 1. Alert Manager (Alert Shell)

To interface with the alert api first run the code below and you'll get the alert manager shell. Enter '?' to get a list of commands as well:

```
$ python dalek.py --alert manager


DALEK (alert-manager) >>> ?
get_info
add_alert
disable_alert
edit_alert
options
?
exit

```

### 2. View alerts

The `get_info` command will return all alerts back to the terminal that associated with the configured api key.

```

DALEK (alert-manager) >>> get_info

Name: <Title>
 ID: <ID>
 Ip: ['1.1.1.1', ... ]
 Triggers: {'malware': {}, 'open_database': {}, 'iot': {}, 'uncommon': {}, 'internet_scanner': {}, 'industrial_control_system': {}, 'new_service': {}, 'ssl_expired': {}, 'vulnerable': {}}
 Date Created: <Date>
```

### 3. Add Alerts

```
$ python dalek.py --alert-manager

DALEK (alert-manager) >>> add_alert

DALEK (Enter Name: ) >>> test

DALEK (Enter IP or [R]: Select from Reports) >>> 1.0.0.1
Name: test
 ID: <ID>
 Ip: ['1.0.0.1']
 Triggers: {}
 Date Created: 2020-05-17T21:29:31.148856


```
#### Add triggers.
---

Now that our alert is created we have to add a 'rule'/'trigger' for our alerts to fire.

```
DALEK (<ID>) >>> add_trigger
Name: any
 Rule: *
 Description: Match any service that is discovered

Name: industrial_control_system
 Rule: tag:ics
 Description: Services associated with industrial control systems

Name: malware
 Rule: tag:compromised,malware
 Description: Compromised or malware-related services

Name: uncommon
 Rule: -port:22,80,443,7547
 Description: Services that generally shouldn't be publicly available

Name: open_database
 Rule: tag:database -port:3306,5432,9306,1434
 Description: Database service that does not require authentication

Name: iot
 Rule: tag:iot
 Description: Service associated with Internet of Things devices

Name: internet_scanner
 Rule: tags:scanner
 Description: Device has been seen scanning the Internet and exposes a service

Name: ssl_expired
 Rule: ssl.cert.expired:true
 Description: Expired SSL certificate is used by the service

Name: vulnerable
 Rule: vulns.*.verified:true
 Description: Service is vulnerable to a known issue

Name: new_service
 Rule: *new
 Description: New open port/ service discovered


DALEK (Select Trigger) >>> iot
Added trigger iot

DALEK (<ID>) >>>

```

Now anytime that this device triggers on one of the `iot` rules it will save it as an alert.


### Edit alerts

To remove triggers from a specific alert follow these steps. (This is a case of an alert that had the `any` trigger assigned to it.)

```
DALEK (alert-manager) >>> edit_alert
in info

Name: <name>
 ID: <ID>
 Ip: [IPs]
 Triggers: {'malware': {}, 'open_database': {}, 'iot': {}, 'uncommon': {}, 'internet_scanner': {}, 'industrial_control_system': {}, 'new_service': {}, 'ssl_expired': {}, 'vulnerable': {}}
 Date Created: <date>

DALEK (Enter Alert id: ) >>> <ID>
add_trigger
remove_trigger

DALEK (<ID>) >>> remove_trigger
Name: <name>
 ID: <ID>
 Ip: [IPS]
 Triggers: {'malware': {}, 'open_database': {}, 'iot': {}, 'uncommon': {}, 'internet_scanner': {}, 'industrial_control_system': {}, 'new_service': {}, 'ssl_expired': {}, 'vulnerable': {}}
 Date Created: <date>

DALEK (Select trigger to remove (CHECK CASE!!!)) >>> iot
Edited trigger iot

DALEK (<ID>) >>>

```

Now the iot ruleset has been removed from the alert and will not log any of those events to the alert dashboard.


### Disable Alerts

**(!! WARNING !!)** This will remove this alert forever. **(!! WARNING !!)**

```

DALEK (alert-manager) >>> disable_alert

Name: test
 ID: D7D06J630ZD18BUM
 Ip: ['1.0.0.1']
 Triggers: {}
 Date Created: 2020-05-17T21:29:31.148000

DALEK (Select ID To remove: ) >>> D7D06J630ZD18BUM
{}

DALEK (alert-manager) >>>
````

### Post Mortum

Additional steps need to be done on shodan.io in the developer dashboard to:
* Export Data
* Setup Email alerts

## Exploits

Ever get stuck just googling for hours on end for POC code for a vulnerability that you've discovered on a pentest or a vulnerability scan? Well shodan thought of this. So here it is in dalek.

```
$ python dalek.py --find-exploit MS08-068
Total: 5

ID: 7125


Description:

Microsoft Windows - SmbRelay3 NTLM Replay (MS08-068)


Author: Andres Tarasco


Platform: windows


Affected Port(s): 0


Exploit Type: remote


Code: * SMBRELAY 3 - NTLM replay attack (version 1.0 ) public version
* (c) 2008 Andres Tarasco AcuÃ±a ( atarasco _at_ gmail.com )
* URL: http://tarasco.org/Web/tools.html

https://github.com/offensive-security/exploitdb-bin-sploits/raw/master/bin-sploits/7125.zip (2008-smbrelay3.zip)

# milw0rm.com [2008-11-14]

```

Additionally it also will grab the source code where available from ExploitDB. (Which is awesome!!!)

So remember...hack/attack things that you are allowed to attack and expressed consent from the owner of a system.

# Note

  ***More coming as More Versions are Released...***

  ***-Cap***
