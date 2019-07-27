import requests
import os
from datetime import datetime
import time
import shodan
import json
from helpers import get_prompt, print_options
from reports  import get_all_reports

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


def add_trigger(api_key, alert_id=None):
    api = shodan.Shodan(api_key)

    if alert_id==None:
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
    print("in info")
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



    prompt = get_prompt("alert-manager")

    available_functions_strings = ['get_info', 'add_alert', 'disable_alert', 'edit_alert', 'options', '?', 'exit']
    edit_alert_functions = ['add_trigger', 'remove_trigger']

    while prompt != "exit":
        if prompt=="options" or prompt=="?":
            print_options(available_functions_strings, api_key)
        elif prompt=="get_info":
            get_all_info(api_key)
        elif prompt=="add_alert":
            name = get_prompt("Enter Name: ")
            ip = get_prompt("Enter IP or [R]: Select from Reports")
            if ip == "R":
                ip = get_all_reports()
            create_monitor_ip(api_key=api_key, name=name, ip=ip)
        elif prompt=="disable_alert":
            get_all_info(api_key)
            id = get_prompt("Select ID To remove: ")
            if id is not None:
                delete_monitor(api_key, id)
        elif prompt=="edit_alert":
            get_all_info(api_key)

            alert_id = get_prompt("Enter Alert id: ")

            print_options(edit_alert_functions, api_key)

            prompt = get_prompt(alert_id)

            while prompt != "back":
                if prompt == "add_trigger":
                    add_trigger(api_key=api_key, alert_id=alert_id)
                elif prompt =="remove_trigger":

                    grab_info(api_key=api_key, alert_id=alert_id)

                    trigger = get_prompt("Select trigger to remove (CHECK CASE!!!)")

                    disable_trigger(api_key=api_key, alert_id=alert_id, trigger=trigger)
                prompt = get_prompt(alert_id)





        prompt = get_prompt("alert-manager")

    exit()

if __name__ == '__main__':
    get_all_reports()
