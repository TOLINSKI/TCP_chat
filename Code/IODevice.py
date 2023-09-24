from abc import ABC, abstractmethod


class IODevice(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def connect(self):
        pass
