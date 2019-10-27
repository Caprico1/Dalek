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
    date_string = "{0}_{1}_{2}".format(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day)
    if os.path.isdir("reports") == False:
        os.mkdir("reports")
    # create dir of datetime if it doesn't exist
    if os.path.isdir("reports/" + date_string) == False:
        os.mkdir("reports/" + date_string)

    report = "reports/" + date_string +'/'+ ip +'.txt'
    try:
        with open(report, 'a+', encoding="utf-8") as file:
            file.write("{}\n".format(ip))
            file.write("{}\n".format(data))
            file.write("\n")
            file.close()
        if docker is not None:
            write_docker_file(docker,ip, date_string)

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

def write_docker_file(docker, ip, date_string):
    dockerfile = "reports/" + date_string + "/docker.txt"

    with open(dockerfile, "a+") as docker_file:
        docker_file.write(ip + "\n")

        if docker['Containers']:
            for container in docker['Containers']:
                docker_file.write("\tImage: {}\n".format(container['Image']))
                docker_file.write("\tID: {}\n".format(container['Id']))
                docker_file.write("\tCommand: {}".format(container['Command']))
                docker_file.write("\tCreated:{}\n".format(container['Created']))
                docker_file.write("Names: \n")

                for name in container['Names']:
                    docker_file.write("\t{}\n".format(name))

                docker_file.write("\tStatus: {}\n".format(container['Status']))
                docker_file.write("Ports:\n")

                for port in container['Ports']:
                    docker_file.write("\t{}\n".format(port))
        elif docker['Containers'] == "":
            pass
        else:
            pass

        # docker_file.write("COMPONENTS: \n")
        # for components in docker['Components']:
        #     docker_file.write("{}\n".format(components['Name']))
        #     docker_file.write('\tDetails:\n')
        #     # docker_file.write("\t\tExperimental: {}\n".format(components['Details']['Experimental']))
        #     docker_file.write("\t\tOS: {}\n".format(components['Details']['Os'] ))
        #     docker_file.write("\t\tMinAPIVersion {}\n".format(components['Details']['MinAPIVersion']))
        #     docker_file.write("\t\tKernelVersion: {}\n".format(components['Details']['KernelVersion']))
        #     docker_file.write("\t\tGoVersion: {}\n".format(components['Details']['GoVersion'] ))
        #     docker_file.write("\t\tGitCommit: {}\n".format(components['Details']['GitCommit'] ))
        #     docker_file.write("\t\tBuildTime: {}\n".format(components['Details']['BuildTime'] ))
        #     docker_file.write("\t\tApiVersion: {}\n".format(components['Details']['ApiVersion']))
        #     docker_file.write("\t\tArch: {}\n".format(components['Details']['Arch']))
    docker_file.close()

def check_time(kill_time):
    if datetime.now() == kill_time:
        print("Killing program now")
        exit()

def all_results(api_key, query_file=None, keyword=None):
    limit = int(input("How many results: "))
    api = shodan.Shodan(api_key)
    page = 0
    date_string = "{0}_{1}_{2}".format(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day)
    if os.path.isdir("reports") == False:
        os.mkdir("reports")
    # create dir of datetime if it doesn't exist
    if os.path.isdir("reports/" + date_string) == False:
        os.mkdir("reports/" + date_string)

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
                if 'docker' in result.keys():
                    docker = result['docker']
                else:
                    docker = None
                create_report(ip, data, docker)

        out_file.close()



if __name__ == '__main__':

    all_results("5Dl3YPn8ZAZkO0tZ8ktxeJXYYg7uNYWu", keyword="docker port:2375")
