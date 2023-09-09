from CommConnector import CommConnector
import socket
import CommConsts

class TCPConnector(CommConnector):
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        
    def connect(self):
        self.client.connect((CommConsts.SERVER, CommConsts.PORT))