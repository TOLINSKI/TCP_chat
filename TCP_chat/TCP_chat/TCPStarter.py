from CommStarter import CommStarter
import socket
import CommConsts

class TCPStarter(CommStarter):
    
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(CommConsts.ADDR)
        
    def start(self):
        self.server.listen()