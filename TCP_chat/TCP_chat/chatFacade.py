from ConsoleMenu import ConsoleMenu

class ChatFacade:
    
    def __init__(self):
        menu = ConsoleMenu()
        menu.startUI()
        menu.validateChoice()
        self.userChoice = menu.getChoice()
        print(f"You have chosen: {self.userChoice}")
    
    