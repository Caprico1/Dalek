import requests
import os
from datetime import datetime
import time
import shodan
import json
from helpers import get_prompt, print_options

created_alert = "Added ip to {0} {1}"
trigger_added = "Added trigger {0}"
trigger_edited = "Edited trigger {0}"

"""
:param: ip can be string or list...mayber..
"""
def create_monitor_ip(api_key, ip, name):
    api = shodan.Shodan(api_key)

    alert = api.create_alert(name=name, ip=ip)

    name = alert['name']
    id = alert['id']
    ip = alert['filters']['ip']
    triggers = alert['triggers']
    created = alert['created']

    all_info = "Name: {0}\n ID: {1}\n Ip: {2}\n Triggers: {3}\n Date Created: {4}".format(name, id, ip, triggers, created)

    print(all_info)
    return 1

def delete_monitor(api_key, id):
    api = shodan.Shodan(api_key)

    response = api.delete_alert(aid = id)

    print(response)
    return 1


def grab_info(api_key, alert_id):
    api = shodan.Shodan(api_key)
    alert = api.alerts(aid=alert_id)


    name = alert['name']
    id = alert['id']
    ip = alert['filters']['ip']
    triggers = alert['triggers']
    created = alert['created']

    all_info = "Name: {0}\n ID: {1}\n Ip: {2}\n Triggers: {3}\n Date Created: {4}".format(name, id, ip, triggers, created)

    print(all_info)
    return 1


def add_trigger(api_key):
    api = shodan.Shodan(api_key)

    get_all_info(api_key)
    alert_id = get_prompt("Select Alert ID")

    get_all_triggers(api_key)
    trigger = get_prompt("Select Trigger")

    api.enable_alert_trigger(aid=alert_id, trigger=trigger)

    print(trigger_added.format(trigger))
    return 1

def disable_trigger(api_key, alert_id, trigger):
    api = shodan.Shodan(api_key)
    api.disable_alert_trigger(aid=alert_id, trigger=trigger)

    print(trigger_edited.format(trigger))
    return 1

def get_all_info(api_key):

    api = shodan.Shodan(api_key)
    all_alerts = api.alerts()

    for alert in all_alerts:
        name = alert['name']
        id = alert['id']
        ip = alert['filters']['ip']
        triggers = alert['triggers']
        created = alert['created']

        all_info = "Name: {0}\n ID: {1}\n Ip: {2}\n Triggers: {3}\n Date Created: {4}".format(name, id, ip, triggers, created)

        print(all_info)
    return 1

def get_all_triggers(api_key):
    api = shodan.Shodan(api_key)
    all_triggers = api.alert_triggers()

    for trigger in all_triggers:

        print("Name: {0}\n Rule: {1}\n Description: {2}\n".format(trigger['name'], trigger['rule'], trigger['description']))

def alert_manager(api_key):

    api = shodan.Shodan(api_key)

    available_functions = {'get_info': get_all_info(api_key), 'add_alert': add_trigger(api_key), 'disable_alert': disable_alert(api_key), 'options': print_options(options, api_key), '?': print_options(options, api_key)}
    get_all_info(api_key)

    prompt = get_prompt("alert-manager")

    if prompt is "options" or prompt is "?":
        print_options(available_functions)


        exit()
if __name__ == '__main__':
    alert_manager("5Dl3YPn8ZAZkO0tZ8ktxeJXYYg7uNYWu")
    main()
