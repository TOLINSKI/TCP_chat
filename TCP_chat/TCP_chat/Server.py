from unittest import defaultTestLoader
import threading
from TCPStarter import TCPStarter

import socket

class Server(TCPStarter):
    
    def __init__(self):
        super().__init__()
        super().start()
        self.clients = {}

    def broadcast(self, message):
        for nickname, client in self.clients:
            client.send(message)
    
    def handle(self, client):
        while True:
            try:
                message = client.recv(TCPStarter.CommConsts.SIZE)
                self.broadcast(message)
            except:
                self.broadcast(f"{client.nickname} left the chat!")
                self.clients.pop(client.nickname)
                client.close()
                break
                
    def startClientThread(self, client):
        thread = threading.Thread(targert=self.handle, args=(client,))
        thread.start() 
    
    def receive(self):
        print("Server is listening...")
   
        while True:
            client, address = self.server.accept()
            print(f"Connected with {client.nickname} IP: {address}")
            
            client.send("NICK".encode(TCPStarter.CommConsts.FORMAT))
            nickname = client.recv(TCPStarter.CommConsts.SIZE)
            self.clients[nickname] = client
            self.broadcast(f"{nickname} has joined the chat!")
            client.send("Connected successfully!".encode(TCPStarter.CommConsts.FORMAT))
            self.startClientThread(client)
            
            
            
    
