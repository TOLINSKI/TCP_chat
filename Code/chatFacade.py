from multiprocessing.connection import Client
from ConsoleMenu import ConsoleMenu
from Server import Server
from Client import Client


class ChatFacade:

    def __init__(self):
        # self.userChoice = 0
        self.devices = {1: Server, 2: Client}
        self.device = None
        self.ui = None

    def startChat(self):
        self.ui = ConsoleMenu()
        self.ui.startUI()
        userChoice = self.ui.getChoice()
        self.device = self.devices[userChoice]()
        self.device.start()
        self.ui.printChoice()

