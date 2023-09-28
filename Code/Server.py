import threading
from IODevice import IODevice
import socket
from configparser import ConfigParser
import ConsoleMenu as ui


class Server(IODevice):

    def __init__(self):
        super().__init__()
        self.clients = {}
        self.server = None

        self.serverConfig = None
        self.messageConfig = None
        self.operationConfig = None
        self.notificationsConfig = None
        self.config = ConfigParser()

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.serverConfig['server'], int(self.serverConfig['port']))
        self.server.bind(address)

    def start(self):
        self.readConfig()
        self.connect()
        self.server.listen()
        self.receive()

    def readConfig(self):
        self.config.read("config.ini")
        try:
            self.serverConfig = self.config["SERVER"]
            self.messageConfig = self.config["MESSAGE"]
            self.operationConfig = self.config["OPERATION"]
            self.notificationsConfig = self.config["NOTIFICATIONS"]
        except:
            print("Error in Server.readConfig")
            exit(0)

    def broadcast(self, message):
        for nickname, client in self.clients.items():
            client.send(message.encode(self.messageConfig['format']))

    def handle(self, client, nickname):
        while True:
            try:
                message = client.recv(int(self.messageConfig['size'])).decode(self.messageConfig['format'])
                if message == self.operationConfig['exit']:
                    self.clients[nickname].send(self.operationConfig['exit'])
                else:
                    self.broadcast(message)
            except:
                self.broadcast(nickname + " " + self.notificationsConfig['left'])
                self.clients.pop(nickname)
                print("clients left:")
                for n, c in self.clients.items():
                    print(n)
                client.close()
                break

    def startClientThread(self, client, nickname):
        thread = threading.Thread(target=self.handle, args=(client, nickname,))
        thread.start()

    def receive(self):
        ui.printListen()

        while True:
            client, address = self.server.accept()
            client.send(self.operationConfig['chooseNickname'].encode(self.messageConfig['format']))
            nickname = client.recv(int(self.messageConfig['size'])).decode(self.messageConfig['format'])
            ui.printClientInfo(address, nickname)
            self.clients[nickname] = client
            self.broadcast(nickname + " " + self.notificationsConfig['joined'])
            client.send(self.notificationsConfig['connected'].encode(self.messageConfig['format']))
            self.startClientThread(client, nickname)
