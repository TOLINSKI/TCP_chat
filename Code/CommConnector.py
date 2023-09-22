from abc import ABC, abstractmethod

class CommConnector(ABC):
    @abstractmethod
    def connect():
        pass