from shutil import copyfile
import json
import os
from os import path


def checkConfig(server):
    if not path.exists('SETTINGS/' + server.id):
        os.makedirs('SETTINGS/' + server.id)
    if not path.isfile('SETTINGS/' + server.id + '/config'):
        copyfile('SETTINGS/config_default', 'SETTINGS/' + server.id + '/config')

def getConfig(server):

    checkConfig(server)
    with open('SETTINGS/' + server.id + '/config') as file:
        return json.load(file)


def saveConfig(server, data):

    checkConfig(server)
    with open("SETTINGS/" + server.id + "/config", "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
