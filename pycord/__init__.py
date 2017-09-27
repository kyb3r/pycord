__title__ = "pycord"
__license__ = "MIT"
__version__ = "0.2.4a"
__author__ = ["verixx", "king1600", "henry232323"]
__github__ = 'https://github.com/verixx/pycord'

from .client import Client
from .models import Embed


def init(lib):
    import multio
    import asks
    multio.init(lib)
    asks.init(lib)
