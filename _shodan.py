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
                if 'docker' in result.keys():
                    docker = result['docker']
                else:
                    docker = None
                create_report(ip, data, docker)
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
        if docker is not None:
            print("writing docker_file")
            write_docker_file(docker,ip, date_string)

        with open("reports/" + date_string + "/all_ips.txt") as ip_file:
            print("{}: Report Created\n".format(ip))
            ip_file.write(ip + "\n")
            ip_file.close()

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

def write_docker_file(docker, ip, date_string):
    dockerfile = "reports/" + date_string + "/docker.txt"

    with open(dockerfile, "a+") as docker_file:
        docker_file.write(ip + "\n")

        for container in docker['Containers']:
            docker_file.write("\tImage: " + container['Image'] + "\n")
            docker_file.write("\tID: " + container['Id']+ "\n")
            docker_file.write("\tCommand: " + container['Command']+ "\n")
            docker_file.write("\tCreated: " + str(container['Created'])+ "\n")
            docker_file.write("Names: \n")
            for name in container['Names']:
                docker_file.write("\t" + name + "\n")
            docker_file.write("\tStatus: " + container['Status'] + "\n")
            docker_file.write("Ports: " + "\n")
            for port in container['Ports']:
                docker_file.write("\t" + port + "\n")

        docker_file.write("COMPONENTS: \n")
        for components in docker['Components']:
            docker_file.write(components['Name'] + "\n")
            docker_file.write('\tDetails:\n')
            docker_file.write("\t\tExperimental: " + components['Details']['Experimental'] + "\n")
            docker_file.write("\t\tOS: " + components['Details']['Os'] + "\n")
            docker_file.write("\t\tMinAPIVersion " + components['Details']['MinAPIVersion']+ "\n")
            docker_file.write("\t\tKernelVersion: " + components['Details']['KernelVersion']+ "\n")
            docker_file.write("\t\tGoVersion: " + components['Details']['GoVersion'] + "\n")
            docker_file.write("\t\tGitCommit: " + components['Details']['GitCommit'] + "\n")
            docker_file.write("\t\tBuildTime: " + components['Details']['BuildTime'] + "\n")
            docker_file.write("\t\tApiVersion: " + components['Details']['ApiVersion'] + "\n")
            docker_file.write("\t\tArch: " + components['Details']['Arch'] + "\n")
    docker_file.close()

def check_time(kill_time):
    if datetime.now() == kill_time:
        print("Killing program now")
        exit()
