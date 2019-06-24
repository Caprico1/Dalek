import requests
import os
from datetime import datetime
import time
import shodan
import json


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


def add_trigger(api_key, alert_id, trigger):
    api = shodan.Shodan(api_key)
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
