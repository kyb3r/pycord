"""
MIT License

Copyright (c) 2017 verixx / king1600

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from ..utils import parse_time
from .core import Serializable


class Embed(Serializable):
    """Class that formats an embed"""
    __slots__ = (
        'color','title','url','author',
        'description','fields','image',
        'thumbnail','footer','timestamp',
        )
    
    def __init__(self, **kwargs):
        """Initialises an Embed object"""
        self.color = kwargs.get('color')
        self.title = kwargs.get('title')
        self.url = kwargs.get('title_url')
        self.description = kwargs.get('description')
        self.timestamp = kwargs.get('timestamp')
        self.fields = []

    @classmethod
    def from_dict(cls, data):
        self = cls.__new__(cls)
        for attr in data:
            if attr == 'timestamp': #special case
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
            'name': name, 
            'value': value, 
            'inline': inline
            }
        self.fields.append(field)
        return self
    
    def set_author(self, name, icon_url=None, url=None):
        """Sets the author of the embed"""
        self.author = {
            'name': name,
            'icon_url' : icon_url,
            'url' : url
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
            'text': text,
            'icon_url': icon_url
            }
        return self
    
    def to_dict(self):
        """Turns the object into a dictionary"""
        return {
            key: getattr(self, key)
            for key in self.__slots__
            if hasattr(self, key) and getattr(self, key)
            }
