

from .core import Serializable
from ..utils import parse_time


class Embed(Serializable):
    """Class that formats an embed"""
    __slots__ = (
        'color', 'title', 'url', 'author',
        'description', 'fields', 'image',
        'thumbnail', 'footer', 'timestamp',
        'type', 'video', 'provider'
    )

    def __init__(self, **kwargs):
        """Initialises an Embed object"""
        self.color = kwargs.get('color')
        self.title = kwargs.get('title')
        self.url = kwargs.get('title_url')
        self.description = kwargs.get('description')
        self.timestamp = kwargs.get('timestamp')
        self.fields = []

    def __repr__(self):
        fmt = ''
        for attr in self.__slots__:
            val = getattr(self, attr, None)
            if val:
                fmt += ' {}={}'.format(attr, val)
                break
        return '<Embed{}>'.format(fmt)

    @classmethod
    def from_dict(cls, data):
        self = cls.__new__(cls)
        for attr in data:
            if attr == 'timestamp':  # special case
                setattr(self, attr, parse_time(data[attr]))
            else:
                setattr(self, attr, data[attr])

    def del_field(self, index):
        """Deletes a field by index"""
        self.fields.pop(index)
        return self

    def add_field(self, name, value, inline=True):
        """Adds a field"""
        field = {
            'name': str(name),
            'value': str(value),
            'inline': inline
        }
        self.fields.append(field)
        return self

    def set_author(self, name, icon_url=None, url=None):
        """Sets the author of the embed"""
        self.author = {
            'name': str(name),
            'icon_url': icon_url,
            'url': str(url)
        }
        return self

    def set_thumbnail(self, url):
        """Sets the thumbnail of the embed"""
        self.thumbnail = {'url': url}
        return self

    def set_image(self, url):
        """Sets the image of the embed"""
        self.image = {'url': url}
        return self

    def set_footer(self, text, icon_url=None):
        """Sets the footer of the embed"""
        self.footer = {
            'text': str(text),
            'icon_url': icon_url
        }
        return self

    def to_dict(self):
        """Turns the object into a dictionary"""
        d = {
            key: getattr(self, key)
            for key in self.__slots__
            if hasattr(self, key) and getattr(self, key)
        }
        ts = d.get('timestamp')
        if ts:
            d['timestamp'] = ts.isoformat()
        
        return d
