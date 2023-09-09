from multiprocessing.connection import Client
from ConsoleMenu import ConsoleMenu
from Server import Server
from Client import Client

class ChatFacade:
    
    def __init__(self):
        menu = ConsoleMenu()
        menu.startUI()
        menu.validateChoice()
        self.userChoice = menu.getChoice()
        if self.userChoice == 1:
            self.server = Server()
            self.server.receive()
        elif self.userChoice == 2:
            self.client = Client()
        print(f"You have chosen: {self.userChoice}")
    
    