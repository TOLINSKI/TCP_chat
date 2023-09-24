import threading
from IODevice import IODevice
import socket
import CommConsts


class Server(IODevice):

    def __init__(self):
        super().__init__()
        self.clients = {}
        self.server = None

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(CommConsts.ADDR)

    def start(self):
        self.connect()
        self.server.listen()
        self.receive()

    def broadcast(self, message):
        for nickname, client in self.clients.items():
            client.send(message.encode(CommConsts.FORMAT))

    def handle(self, client, nickname):
        while True:
            try:
                message = client.recv(CommConsts.SIZE).decode(CommConsts.FORMAT)
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
            client.send("NICK".encode(CommConsts.FORMAT))
            nickname = client.recv(CommConsts.SIZE).decode(CommConsts.FORMAT)
            print(f"The client's nickname is: {nickname}'")
            self.clients[nickname] = client
            self.broadcast(f"{nickname} has joined the chat!")
            client.send("Connected successfully!".encode(CommConsts.FORMAT))
            self.startClientThread(client, nickname)
