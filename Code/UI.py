from abc import ABC, abstractmethod


class UI(ABC):
    @abstractmethod
    def startUI(self):
        pass
