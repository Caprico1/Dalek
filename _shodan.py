import requests
import os
from datetime import datetime
import time
import shodan
import json
import helpers

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
                if 'docker' in result.keys():
                    docker = result['docker']
                else:
                    docker = None
                create_report(ip, data, docker)
        except shodan.APIError as e:
            print('Error: {} \n {}'.format(e, line))
            pass
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
                        if 'docker' in result.keys():
                            docker = result['docker']
                        else:
                            docker = None
                        create_report(ip, data, docker)
                except shodan.APIError as e:
                    print('Error: {} \n {}'.format(e, line))

        print ("Total Results: {}".format(total))
        return 1

def shodan_query_manager(api_key, kill_time, increment, query_file):
    check_time(kill_time)
    query_shodan(api_key, query_file)

    do_increment(pause_time, restart_time, increment)

def create_report(ip, data, docker=None):
    # ex. directory 2019_1_1/
    date_string = helpers.get_date_string()

    if helpers.files_check(date_string) != 1:
        exit("Something went wrong.")


    report = "reports/" + date_string +'/'+ ip +'.txt'
    try:
        with open(report, 'a+', encoding="utf-8") as file:
            file.write("{}\n".format(ip))
            file.write("{}\n".format(data))
            file.write("\n")
            file.close()

        with open("reports/" + date_string + "/all_ips.txt", 'a+') as ip_file:
            ip_file.write("{}\n".format(ip))
            ip_file.close()

    except Exception as e:
        print("Exception: {}".format(e))
        for key,val in docker.items():
            print(key + "=>", val)

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

def all_results(api_key, query_file=None, keyword=None):
    limit = int(input("How many results: "))
    api = shodan.Shodan(api_key)
    date_string = helpers.get_date_string()

    if helpers.files_check(date_string) != 1:
        exit("Something went wrong.")

    if keyword is not None:
        output_file = "reports/" + date_string + "/-export" + keyword.replace(" ", "_").replace(":", "_")
        if os.path.exists(output_file) is False:

            os.system("shodan download --limit {} {} {}".format(limit,output_file, keyword))
            os.system("gzip -d {}".format(output_file + ".json.gz"))
        else:
            print("That query has already been ran...exiting\n\n")
            sleep(3)
            exit()
        with open(output_file + ".json", "r") as out_file:
            for line in out_file.readlines():
                result = json.loads(line)
                ip = result['ip_str']
                data = result['data']

                create_report(ip, data)

        out_file.close()
