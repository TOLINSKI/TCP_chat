import threading
from IODevice import IODevice
import socket
from configparser import ConfigParser
from ipaddress import ip_address


class Server(IODevice):

    def __init__(self):
        super().__init__()
        self.clients = {}
        self.server = None
        self.serverConfig = None
        self.messageConfig = None
        self.config = ConfigParser()

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.serverConfig['server'], int(self.serverConfig['port']))
        self.server.bind(address)

    def start(self):
        self.config.read("config.ini")
        try:
            self.serverConfig = self.config["SERVER"]
            self.messageConfig = self.config["MESSAGE"]
        except:
            print("Error in Config file")
            exit(0)
        self.connect()
        self.server.listen()
        self.receive()

    def broadcast(self, message):
        for nickname, client in self.clients.items():
            client.send(message.encode(self.messageConfig['format']))

    def handle(self, client, nickname):
        while True:
            try:
                message = client.recv(int(self.messageConfig['size'])).decode(self.messageConfig['format'])
                if (message == "/Exit"):
                    self.clients[nickname].send("/Exit")
                else:
                    self.broadcast(message)
            except:
                self.broadcast(f"{nickname} left the chat!")
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
        print("Server is listening...")

        while True:
            client, address = self.server.accept()
            print(f"Connected with IP: {address}")
            client.send("NICK".encode(self.messageConfig['format']))
            nickname = client.recv(int(self.messageConfig['size'])).decode(self.messageConfig['format'])
            print(f"The client's nickname is: {nickname}'")
            self.clients[nickname] = client
            self.broadcast(f"{nickname} has joined the chat!")
            client.send("Connected successfully!".encode(self.messageConfig['format']))
            self.startClientThread(client, nickname)
