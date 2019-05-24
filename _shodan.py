import requests
import os
from datetime import datetime

def query_shodan(api_key, query_file):
    with open(query_file) as file:
        queries = file.readlines()
    #strip any spaces
    queries = [x.strip() for x in queries]

    for query in queries:
        response = requests.get("https://api.shodan.io/shodan/host/search?key={0}&query={1}".format(api_key, query))

        print(response.text)
        exit()

def shodan_query_manager(api_key, kill_time, increment, query_file):
    check_time(kill_time)
    query_shodan(api_key, query_file)

    do_increment(pause_time, restart_time, increment)

def create_report(results):
    date_string = "{0}_{1}_{2}".format(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day)
    if os.isdir("reports") == False:
        os.mkdir("reports")
    # create dir of datetime if it doesn't exist
    if os.isdir(date_string)
        os.mkdir(date_string)
    # grab ip
    # name the file Ip
def do_increment(pause_time, restart_time, increment):
    if pause_time >= datetime.now():
        sleep(1)
        while datetime.now() >= restart_time:
            do_increment(pause_time, restart_time, increment)
    else:
        pass


def check_time(kill_time):
    if datetime.now() == kill_time
        print("Killing program now")
        exit()
