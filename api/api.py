# API for communication to the control center via COSMOS

# author: Owen Bramley
# date modified: 04/10/2023
# version: 0.1 (alpha)

from os.path import exists
import sensors
import socket
import json
import shelve
import requests
import random

# status codes key
# 0 = error
# 1 = success
# 2 = server update pending
# 3 = bot update pending (typiclly used for initilization)

# persistant data file setup
DATA_FILE = "AEV"

# function to initilize the bot with the server
def init():
    

# check if the data file exists
if (not exists("%s.db",DATA_FILE)):
    s = shelve.open(DATA_FILE)
    bot_id = random.randint(1111, 9999)
    s['hostname'] = socket.gethostname()
    # s['ip'] = socket.gethostbyname(socket.gethostname())
    s['bot_id'] = bot_id
    s['status'] = 2
    s['token'] = random.randint(1111, 9999)
    s['type'] = "undefined"
    s.close()
    # run the initilization function after primary parameters are setup
    init(bot_id)


# server communication setup
# api-endpoint
api_ip = "192.168.0.1"
api_URL = ("http://%s/includes/api/api.php",api_ip)

# full status update of bot, this includes all data that is relevant to runtime operations
def up_status():
    # open shelve to save data
    s = shelve.open(DATA_FILE)
    # get sensor data fromm api.py
    data = sensors.get_a_sensors()
    # set update type for server decoding
    type = "up_status"
    # json data to be sent
    json_data = {'type': type, 'data': data, 'token': token}
    # create request
    request = requests.post(api_URL, params=req_type, json=json_data)
    # decode json received
    # print("pre-refreshed attributes:")
    # decode json
    recived_json = request.json()
    # print(json)

    try:
        # update attributes
        print("refreshed attributes:")

        s['token'] = json['new_token']
        s['status'] = json['status']
        s['type'] = json['type']
        if (json['type'] == "door_node"):
            s['location_id'] = json['location_id']
        if (json['type'] == "machine_node"):
            s['location_id'] = json['location_id']
            s['machine_id'] = json['machine_id']

        # close shelve
        s.close()

    except:
        print("Server Error")


# telemetry update
def up_telem():

