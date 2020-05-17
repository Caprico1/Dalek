def check_time(kill_time):
    if datetime.now() == kill_time:
        print("Killing program now")
        exit()

def shodan_query_manager(api_key, kill_time, increment, query_file):
    check_time(kill_time)
    query_shodan(api_key, query_file)

    do_increment(pause_time, restart_time, increment)

def do_increment(pause_time, restart_time, increment):
    if pause_time >= datetime.now():
        sleep(1)
        while datetime.now() >= restart_time:
            do_increment(pause_time, restart_time, increment)
    else:
        pass
