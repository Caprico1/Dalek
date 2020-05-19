import math
from datetime import datetime
import shodan
import time
import os

def get_prompt(string=None):
    if string is not None:
        cmd = input("\nDALEK ({}) >>> ".format(string))
    else:
        cmd = input("\nDALEK >>> ")
    return cmd

def print_options(list, api_key):
    for item in list:
        print(item)
    return

def calculate_pages(total):
    pages = math.floor(total / 100) + 1

    print(pages)
    return pages

def prompt_for_pages(pages):
    print("Each page = 1 Query Credit")
    page_number = get_prompt("Enter Maximum Page Number: ")

    return page_number


def get_date_string():

    return "{0}_{1}_{2}".format(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day)

def report_dir_check(date_string):
    if os.path.isdir("reports") == False:
        os.mkdir("reports")
    # create dir of datetime if it doesn't exist
    if os.path.isdir("reports/" + date_string) == False:
        os.mkdir("reports/" + date_string)

    return

def get_total_results(api, keyword=None, line=None):

    if keyword is not None:

        total = api.count('{}'.format(keyword))['total']
        time.sleep(3)

    elif line is not None:

        total = api.count('{}'.format(line))['total']
        time.sleep(3)



    return total

def write_to_ip_file(report, ip, data):
    try:
        with open(report, 'a+', encoding="utf-8") as file:
            file.write("{}\n".format(ip))
            file.write("{}\n".format(data))
            file.write("\n")
            file.close()

    except:
        print(report)
        print("write to ip file failed")
        pass
    return
