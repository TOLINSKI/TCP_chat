from configparser import ConfigParser
import socket

config = ConfigParser()

config["MESSAGE"] = {
    'size': 1024,
    'format': 'utf-8',
}

config["SERVER"] = {
    'port': 5050,
    'server': socket.gethostbyname(socket.gethostname()),
}

config["OPERATION"] = {
    'chooseNickname': '/NICK',
    'exit': '/Exit',
}

config["NOTIFICATIONS"] = {
    'joined': ' has joined the chat!',
    'connected': 'Connected Successfully!',
    'left': ' has left teh chat!',
    'enterNickname': 'Enter your nickname:\n',
}

with open('config.ini', 'w') as configFile:
    config.write(configFile)



