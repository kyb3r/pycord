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


class Collection(dict):
    __slots__ = ('data', 'index', 'instance')

    def __init__(self, instance=dict, indexor="id", maxlen=None):
        dict.__init__(self)
        self.index = indexor
        self.instance = instance
    
    def __iter__(self):
        for val in self.values():
            yield val

    def __add__(self, other):
        """ Add a collection to self """
        if isinstance(other, Collection):
            if isinstance(other.instance, self.instance):
                [self.add(item) for item in other]
        elif isinstance(other, self.instance):
            self.add(other)
        else:
            raise ValueError("Item is not collection or instance of")

    def __iadd__(self, other):
        """ += add a collection to self """
        self.__add__(other)

    def __setitem__(self, key, value):
        """ Array setting by key """
        if not isinstance(value, self.instance):
            raise ValueError("{} is not instance of {.instance}".format(value, self))
        dict.__setitem__(self, key, value)

    def add(self, item):
        """ Add an item to the collection """
        if not isinstance(item, self.instance):
            raise ValueError("{} is not instance of {.instance}".format(item, self))
        index = getattr(item, self.index, None)
        if index is None:
            raise AttributeError("{.index} of {} is invalid".format(self, repr(item)))
        self[index] = item

    def remove(self, item):
        """ Remove item from collection """
        if isinstance(item, self.instance):
            if getattr(item, self.index, None) is not None:
                del self[getattr(item, self.index)]
        else:
            if item in self:
                del self[item]

    def remove_if(self, **attrs):
        """ Remove items if meet attribute conditions """
        for key, value in reversed(self.items()):
            if self.has_attrs(value, **attrs):
                del self[key]

    def has_attrs(self, obj, **attrs):
        """ Check if object has attrs """ 
        for key, value in attrs.items():
            if not getattr(obj, key, None) == value:
                return False
        return True

    def has(self, key):
        """ Check if object with id in collection """
        if isinstance(key, self.instance):
            return self.__contains__(key)
        for item in self:
            if getattr(item, self.index, None) == key:
                return True
        return False

    def find(self, condition):
        """ Find all objects which meet callable condition """
        return [item for item in self if condition(item)]

    def find_one(self, condition):
        """ Find first  which meet callable condition """
        for item in self:
            if condition(item):
                return item

    def get(self, id=None, **attrs):
        """ Find using arguments and attr to value filters """
        attrs['id'] = id or attrs.get('id')
        return self.find_one(lambda i: self.has_attrs(i, **attrs))



