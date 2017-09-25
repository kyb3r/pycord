from abc import ABC, abstractmethod

class Converter(ABC):

    @abstractmethod
    def __init__(self, msg, value):
        pass

    @abstractmethod
    def convert(self):
        pass
