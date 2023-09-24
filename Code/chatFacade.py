from multiprocessing.connection import Client
from ConsoleMenu import ConsoleMenu
from Server import Server
from Client import Client


class ChatFacade:

    def __init__(self):
        self.userChoice = 0
        self.server = None
        self.client = None
        self.menu = ConsoleMenu()

    def startChat(self):
        self.menu.startUI()
        self.menu.validateChoice()
        self.userChoice = self.menu.getChoice()
        if self.userChoice == 1:
            self.server = Server()
            self.server.start()
            self.server.receive()
        elif self.userChoice == 2:
            self.client = Client()
            self.client.start()
        self.menu.printChoice()
