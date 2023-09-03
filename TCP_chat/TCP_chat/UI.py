from abc import ABC, abstractclassmethod

class UI(ABC):
    @abstractclassmethod
    def startUI():
        pass