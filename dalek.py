from argparse import ArgumentParser
from config import get_api_key
from datetime import datetime
from _shodan import shodan_query_manager, query_shodan, all_results
from monitor import alert_manager
import exploit_api
def main():

    api_key = None
    kill_time = None
    increment = None
    keyword = None

    parser = ArgumentParser(description="A shodan scraper looking for botnets utilizing and exploiting vulnerable and misconfigured docker.socket instances")


    parser.add_argument('--api_key', help="Api key from api.shodan.io goes here")

    # parser.add_argument('--kill-time', help="How long you want the program to scan")

    parser.add_argument(
    '--increment',
     help="How far increments of scans will be in hours. (Example: 1, 2, 3)"
     )

    parser.add_argument('--file', help="File with all shodan api query strings")

    parser.add_argument('--keyword', help="Single query string to search shodan with")


    parser.add_argument(
        '--all_results',
         action="store_true",
         help="Get larger amount of results.\
         Usage: --all_results --keyword "" or --all_results --file <path> \
        (!! WARNING: This will use up a large number of query credits !!)")

    parser.add_argument(
        '--limit',
        help="Get a certain number of results\
            Usage: --all_results --limit 100 --keyword "" or --all_results --limit 100 --file <path>\
            (!! WARNING: This will use up a large number of query credits !!)"
    )

    monitor = parser.add_argument_group('Monitor', description="Set up alerts for monitoring ips from scans.")

    ## TODO
    # monitor.add_argument('--create-alert NAME', help="Create a new alert")
    # monitor.add_argument('--list-alerts', help="List all alerts associated with this account")
    # monitor.add_argument('--add-trigger TRIGGER', help="add trigger to specific alert")
    # monitor.add_argument('--disable-trigger TRIGGER', help="disable trigger from alert id.")

    monitor.add_argument('--alert-manager', action="store_true", help="Semi gui input thing for creating alerts")

    exploits = parser.add_argument_group('Exploits', description="Query Exploits from Shodans Exploit API")

    exploits.add_argument('--find-exploit', help="Find Exploits Based off keyword search")


    args = parser.parse_args()


    if args.find_exploit is not None:
        results = exploit_api.query_exploits(get_api_key(),args.find_exploit)

        print(results)



    if args.api_key is None:
        args.api_key = get_api_key()

    if args.api_key is not None:
        if args.alert_manager is True:
            alert_manager(args.api_key)

        if args.limit is not None:

            if args.all_results is True and args.keyword is not None:
                all_results(api_key=args.api_key, keyword=args.keyword, limit_results=args.limit)

            elif args.all_results is True and args.file is not None:
                all_results(api_key=args.api_key, query_file=args.keyword, limit_results=args.limit)
        elif args.limit is None:
            if args.all_results is True and args.keyword is not None:
                all_results(api_key=args.api_key, keyword=args.keyword)

            elif args.all_results is True and args.file is not None:
                all_results(api_key=args.api_key, query_file=args.keyword)
        else:
              print("Dalek cannot download results without query file or keyword...")
              exit()

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
    else:
        print("API KEY REQUIRED!!!")
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
