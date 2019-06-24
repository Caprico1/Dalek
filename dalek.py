from argparse import ArgumentParser
from datetime import datetime
from _shodan import shodan_query_manager, query_shodan
def main():

    api_key = None
    kill_time = None
    increment = None
    keyword = None

    parser = ArgumentParser(description="A shodan scraper looking for botnets utilizing and exploiting vulnerable and misconfigured docker.socket instances")

    parser.add_argument('--api_key', help="Api key from api.shodan.io goes here")
    parser.add_argument('--kill-time', help="How long you want the program to scan")
    parser.add_argument('--increment', help="How far increments of scans will be in hours. (Example: 1, 2, 3)")
    parser.add_argument('--file', help="File with all shodan api query strings")
    parser.add_argument('--keyword', help="Single query string to search shodan with")

    monitor = parser.add_argument_group('Monitor', description="Set up alerts for monitoring ips from scans.")

    monitor.add_argument('--create-alert', help="Create a new alert")
    monitor.add_argument('--list-alerts', help="List all alerts associated with this account")
    monitor.add_argument('--add-trigger', help="add trigger to specific alert")
    monitor.add_argument('--disable-trigger', help="disable trigger from alert id.")

    args = parser.parse_args()


    if args.keyword is not None:
        keyword = args.keyword
        api_key = args.api_key

        if keyword is None or api_key is None:
            print("Need keyword and api_key key...\n Check your arguments...pls")
            exit()

        query_shodan(api_key=api_key, keyword=keyword)
    elif args.file is not None:
        api_key = args.api_key
        query_file = args.file

        if query_file is None or api_key is None:
            print("Need file path and api_key key...\n Check your arguments...pls")
            exit()

        query_shodan(api_key=api_key, query_file=query_file)


    print("All done...byb")
    exit()
    # later
    # try:
    #
    #     api_key = args.api_key
    #     kill_time = args.kill_time
    #     increment = args.increment
    # except:
    #     print("ALL args need to be provided")
    #     exit()
    #
    # shodan_query_manager(api_key, kill_time, increment)

main()
