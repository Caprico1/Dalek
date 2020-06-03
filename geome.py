
from helpers import get_prompt, print_options, get_date_string
import os
import json

"""
:param date ex. YYYY_M(M)_D(D)
"""
def print_exports(date):
    os.listdir("{}_{}_{}".format())


def write_to_geo_file(result, ip):


    try:
        with open("reports/{}/geo_info.txt".format(get_date_string()), "w") as geo_file:
            geo_file.write("IP: {}\n".format(ip))

            geo_file.write("\tLatitude/Longitude : {}/{}\n".format(result['location']['latitude'], result['location']['longitude']))
            geo_file.write("\tCountry: {}\n".format(result['location']['country_name']))
            geo_file.write("\tCountry Code: {}\n".format(result['location']['country_code']))
            geo_file.write("\tCity: {}\n".format(result['location']['city']))

            geo_file.close()
        print("write_to_geo_file")

    except Exception as e:

        print("Exception:{}".format(e) )
