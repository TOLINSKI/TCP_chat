from TCPConnector import TCPConnector
import threading
import socket
import CommConsts

class Client(TCPConnector):
    
    def __init__(self):
        super().__init__()
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
                    self.client.send(userInput.encode(CommConsts.FORMAT))
                    print(f"Goodbye {self.nickname}")
                    self.exitEvent.set()
                    break
                message = f"{self.nickname}: {userInput}"
                self.client.send(message.encode(CommConsts.FORMAT))
            except:
                print("An error occured!")
                break
            
    
    def receive(self):
        print("Receive thread started")
        while not self.exitEvent.is_set():
            try:
                message = self.client.recv(CommConsts.SIZE).decode(CommConsts.FORMAT)
                if(message == 'NICK'):
                    self.client.send(self.nickname.encode(CommConsts.FORMAT))
                elif(message == '/Exit'):
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
    
    
    