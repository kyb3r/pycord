from abc import ABC, abstractmethod

class Converter(ABC):

    @abstractmethod
    def __init__(self, ctx, value):
        pass

    @abstractmethod
    def convert(self):
        pass


def member(ctx, argument):
    '''Converts arguments to a member object.'''
    client = ctx.client
