import requests
import os
from datetime import datetime
import time
import shodan
import json
import helpers
import geome
from docker import write_docker_file
from schedule import shodan_query_manager


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
                geome.write_to_geo_file(result, ip)
                # geome.plot_map(result,ip)
                if 'docker' in result.keys():
                    docker = result['docker']
                else:
                    docker = None
                try:
                    create_report(ip, data, docker)
                except:
                    print("Report failed")
                    exit()
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

def create_report(ip, data, docker=None):
    # ex. directory 2019_1_1/
    date_string = helpers.get_date_string()
    helpers.report_dir_check(date_string)

    report = "reports/" + date_string +'/'+ ip +'.txt'
    try:
        helpers.write_to_ip_file(report, ip, data)

        if docker is not None:
            write_docker_file(docker=docker,ip=ip, date_string=date_string)

        with open("reports/" + date_string + "/all_ips.txt", 'a+') as ip_file:
            ip_file.write("{}\n".format(ip))
            ip_file.close()

        geome.get_location_data_from_file(data, ip)

    except Exception as e:
        pass

def all_results(api_key, keyword=None, limit_results=None):
    api = shodan.Shodan(api_key)

    if limit_results is None:
        limit = helpers.get_total_results(api, keyword=keyword)
    else:
        limit = limit_results
    date_string = helpers.get_date_string()
    helpers.report_dir_check(date_string)


    if keyword is not None:
        output_file = "reports/" + date_string + "/-export" + keyword.replace(" ", "_").replace(":", "_").replace("\"","_").replace(";","").replace(".","").replace("-","").replace("&","")
        if os.path.exists(output_file+ ".json") is False:

            os.system("shodan download --limit {} {} {}".format(limit,output_file, keyword))
            os.system("gzip -d {}".format(output_file + ".json.gz"))
        else:
            print("That query has already been ran...exiting\n\n")
            time.sleep(3)
            exit()
        with open(output_file + ".json", "r") as out_file:
            docker=None
            for line in out_file.readlines():
                result = json.loads(line)
                ip = result['ip_str']
                data = result['data']
                if 'opts' in result.keys():

                    if 'docker' in result['opts'].keys():
                        docker = result['opts']['docker']
                    else:
                        docker = None
                print("Creating report")

                create_report(ip, data, docker=docker)

        out_file.close()
