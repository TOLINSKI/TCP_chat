import threading
import socket
from configparser import ConfigParser
from IODevice import IODevice
import ConsoleMenu as ui


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
        self.notificationsConfig = None
        self.operationConfig = None
        self.config = ConfigParser()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.serverConfig['server'], int(self.serverConfig['port']))
        self.client.connect(address)

    def start(self):
        self.readConfig()
        self.connect()
        ui.printClientConnected(self.client.getpeername())
        self.nickname = input(self.notificationsConfig['enterNickName'])
        self.exitEvent = threading.Event()
        self.startRecvThread()
        self.startWriteThread()

    def readConfig(self):
        self.config.read("config.ini")
        try:
            self.serverConfig = self.config["SERVER"]
            self.messageConfig = self.config["MESSAGE"]
            self.operationConfig = self.config["OPERATION"]
            self.notificationsConfig = self.config["NOTIFICATIONS"]
        except:
            print("Error in Client.readConfig")
            exit(0)

    def write(self):
        # print("Write thread started")
        while not self.exitEvent.is_set():
            try:
                userInput = input()
                if userInput == self.operationConfig['exit']:
                    self.client.send(userInput.encode(self.messageConfig['format']))
                    print(f"Goodbye {self.nickname}")
                    self.exitEvent.set()
                    break
                message = f"{self.nickname}: {userInput}"
                self.client.send(message.encode(self.messageConfig['format']))
            except:
                print("Error in Client.write()")
                break

    def receive(self):
        # print("Receive thread started")
        while not self.exitEvent.is_set():
            try:
                message = self.client.recv(int(self.messageConfig['size'])).decode(self.messageConfig['format'])
                if message == self.operationConfig['chooseNickname']:
                    self.client.send(self.nickname.encode(self.messageConfig['format']))
                elif message == self.operationConfig['exit']:
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
