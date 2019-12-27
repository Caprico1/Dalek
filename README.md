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


# Examples

1. Keyword search
  ```
  $ python dalek.py --keyword "apache"
  ```
  This will grab the first one hundred (100) hosts that 'match' the keyword query.

  Also shoutout to @424f424f for the suggestion of this feature. Made my life so much easier.

2. Query File search

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

3. All Results

  At this point in the project the best way to do this option (and the only one that I've really tested) is with the keyword search.

  This will be updated when I work on the project some more.
  1. Get the initial results and the total
  ```
  $ python dalek.py --keyword "docker"
  ```
  Output:
    ```
    Total Results: <some number>
    All done...byb
    ```

  2. Getting all results

    ```
    $ python dalek.py --keyword "docker" --all_results
    ```
    Shodan requires a number limit. If you want all of the results put the `Total Results: ` value in when you're prompted for `How many Results: `

    *Important*: Sometimes Shodan will not give you all of the results. This is not an issue with the project. This is just the fact that shodan is awesome and everyone knows it ;)

    **Again, keep an eye on your query credits. This will drain your credits very quickly if you give it a large number (x>1000)**


# Note

  ***More coming as More Versions are Released...***

  ***-Cap***
