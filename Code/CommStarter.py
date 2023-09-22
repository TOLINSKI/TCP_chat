from abc import ABC, abstractmethod

class CommStarter(ABC):
    @abstractmethod
    def start():
        pass