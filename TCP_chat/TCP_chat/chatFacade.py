from ConsoleMenu import ConsoleMenu
from Server import Server

class ChatFacade:
    
    def __init__(self):
        menu = ConsoleMenu()
        menu.startUI()
        menu.validateChoice()
        self.userChoice = menu.getChoice()
        if self.userChoice == 1:
            self.server = Server()
            self.server.receive()
        print(f"You have chosen: {self.userChoice}")
    
    