from UI import UI

class ConsoleMenu(UI):
   
    def __init__(self):
        self.userChoice = 0
    

    def validateChoice(self):
        goodInput = False
        while not goodInput:
            userInput = input()
            if len(userInput) != 1:
                    print("Error please enter a number 1-3")
                    continue
            elif ord(userInput) < ord("1") or ord(userInput) > ord("3"):
                print("Error please enter a number 1-3")
                continue
            goodInput = True
            self.userChoice = int(userInput)


    def startUI(self):
        print("1. Start a new chat")
        print("2. Connect to existing chat")
        print("3. Exit")
           

    def getChoice(self):
        return self.userChoice
        
        
    