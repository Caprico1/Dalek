import math
from datetime import datetime
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

def files_check(date_string):

    if os.path.isdir("reports") == False:
        os.mkdir("reports")

    # create dir of datetime if it doesn't exist
    if os.path.isdir("reports/" + date_string) == False:
        os.mkdir("reports/" + date_string)

    return 1
