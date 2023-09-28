import threading
import socket
from configparser import ConfigParser
from IODevice import IODevice


class Client(IODevice):
    
    def __init__(self):
        super().__init__()
        self.client = None
        self.exitEvent = None
        self.nickname = None

        self.writeThread = None
        self.receiveThread = None

        self.messageConfig = None
        self.serverConfig = None
        self.config = ConfigParser()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.serverConfig['server'], int(self.serverConfig['port']))
        self.client.connect(address)
    
    def start(self):
        self.config.read("config.ini")
        try:
            self.serverConfig = self.config["SERVER"]
            self.messageConfig = self.config["MESSAGE"]
        except:
            print("Error in Config file")
            exit(0)
        self.connect()
        print(f"Client initiated with IP:{self.client.getpeername()}")
        self.nickname = input("Enter your nickname:\n")
        self.exitEvent = threading.Event()
        self.startRecvThread()
        self.startWriteThread()

    def write(self):
        print("Write thread started")
        while not self.exitEvent.is_set():
            try:
                userInput = input()
                if userInput == '/Exit':
                    self.client.send(userInput.encode(self.messageConfig['format']))
                    print(f"Goodbye {self.nickname}")
                    self.exitEvent.set()
                    break
                message = f"{self.nickname}: {userInput}"
                self.client.send(message.encode(self.messageConfig['format']))
            except:
                print("An error occured!")
                break

    def receive(self):
        print("Receive thread started")
        while not self.exitEvent.is_set():
            try:
                message = self.client.recv(int(self.messageConfig['size'])).decode(self.messageConfig['format'])
                if message == 'NICK':
                    self.client.send(self.nickname.encode(self.messageConfig['format']))
                elif message == '/Exit':
                    break
                else:
                    print(message)
            except:
                print("An error occured!")
                break

    def startWriteThread(self):
        self.writeThread = threading.Thread(target=self.write)
        self.writeThread.start()

    def startRecvThread(self):
        self.receiveThread = threading.Thread(target=self.receive)
        self.receiveThread.start()

    def getClient(self):
        return self
