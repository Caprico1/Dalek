from argparse import ArgumentParser
from datetime import datetime
from _shodan import shodan_query_manager
def main():

    api_key = None
    kill_time = None
    increment = None

    parser = ArgumentParser(description="A shodan scraper looking for botnets utilizing and exploiting vulnerable and misconfigured docker.socket instances")

    parser.add_argument('--api_key', help="Api key from api.shodan.io goes here")
    parser.add_argument('--kill-time' help="How long you want the program to scan")
    parser.add_argument('--increment' help="How far increments of scans will be in hours. (Example: 1, 2, 3)")
    parser.add_argument('--file' help="File with all shodan api query strings")

    args = parser.parse_args()

    try:

        api_key = args.api_key
        kill_time = args.kill_time
        increment = args.increment
    except:
        print("ALL args need to be provided")
        exit()

    shodan_query_manager(api_key, kill_time, increment)

main()
