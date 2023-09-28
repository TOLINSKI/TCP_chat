from configparser import ConfigParser
import socket

config = ConfigParser()

config["MESSAGE"] = {
    "size": 1024,
    "format": 'utf-8',
    "exit": '/Exit',
}

config["SERVER"] = {
    "port": 5050,
    "server": socket.gethostbyname(socket.gethostname()),
}

with open('config.ini', 'w') as configFile:
    config.write(configFile)



