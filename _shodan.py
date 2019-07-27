import requests
import os
from datetime import datetime
import time
import shodan
import json


def query_shodan(api_key, query_file=None, keyword=None):
    api = shodan.Shodan(api_key)
    total = 0

    if keyword is not None:
        try:
            # Search Shodan
            results = api.search('{}'.format(keyword))
            time.sleep(3)
            # Show the results
            total += results['total']
            for result in results['matches']:
                ip = result['ip_str']
                data = result['data']
                create_report(ip, data)
        except shodan.APIError as e:
            print('Error: {} \n {}'.format(e, line))
        print ("Total Results: {}".format(total))
        return 1
    if query_file is not None:
        with open(query_file, 'r', encoding="utf-8") as query_f:
            for line in query_f:
                try:
                    # Search Shodan
                    results = api.search('{}'.format(line))
                    time.sleep(3)
                    # Show the results
                    total += results['total']
                    for result in results['matches']:
                        ip = result['ip_str']
                        data = result['data']
                        create_report(ip, data)
                except shodan.APIError as e:
                    print('Error: {} \n {}'.format(e, line))
        print ("Total Results: {}".format(total))
        return 1

def shodan_query_manager(api_key, kill_time, increment, query_file):
    check_time(kill_time)
    query_shodan(api_key, query_file)

    do_increment(pause_time, restart_time, increment)

def create_report(ip, data):
    # ex. directory 2019_1_1/
    date_string = "{0}_{1}_{2}".format(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day)
    if os.path.isdir("reports") == False:
        os.mkdir("reports")
    # create dir of datetime if it doesn't exist
    if os.path.isdir("reports/" + date_string) == False:
        os.mkdir("reports/" + date_string)

    report = "reports/" + date_string +'/'+ ip +'.txt'
    try:
        with open(report, 'a+', encoding="utf-8") as file:
            file.write(ip + "\n")
            file.write(data+ "\n")
            file.write("\n")
            file.close()

        with open("reports/" + date_string + "/all_ips.txt") as ip_file:
            print("{}: Report Created\n".format(ip))
            ip_file.write(ip + "\n")

        return 1
    except Exception as e:
        print("File already exists...must've scanned it already")


def do_increment(pause_time, restart_time, increment):
    if pause_time >= datetime.now():
        sleep(1)
        while datetime.now() >= restart_time:
            do_increment(pause_time, restart_time, increment)
    else:
        pass


def check_time(kill_time):
    if datetime.now() == kill_time:
        print("Killing program now")
        exit()
