from configparser import ConfigParser
import socket

config_obj = ConfigParser()

config_obj["MESSAGEINFO"] = {
    "size": 1024,
    "format": 'utf-8',
}

config_obj["SERVERCONFIG"] = {
    "port": 5050,
    "server": socket.gethostbyname(socket.gethostname()),
}

with open('config.ini', 'w') as config:
    config_obj.write(config)



