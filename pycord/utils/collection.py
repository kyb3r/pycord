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

from collections import deque


class Collection:
    __slots__ = ('data', 'index', 'instance')

    def __init__(self, instance=dict, indexor="id", maxlen=None):
        self.data = deque(maxlen=maxlen)
        self.index = indexor
        self.instance = instance

    def __iter__(self):
        """ Object iteration """
        for item in self.data:
            yield item

    def __contains__(self, item):
        """ Check if item in collection """
        return item in self.data

    def __len__(self):
        """ Get the amount of elements """
        return len(self.data)

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

    def __getitem__(self, key):
        """ Array index searching by index """
        found = self.find(lambda i: getattr(i, self.index, None) == key)
        return found[0] if found else None

    def __setitem__(self, key, value):
        """ Array setting by key """
        if not isinstance(value, self.instance):
            raise ValueError(f"{value} is not instance of {self.instance}")
        for pos, item in enumerate(self.__iter__()):
            if getattr(item, self.index, None) == key:
                self.data[pos] = value
                return
        self.data.append(value)

    def add(self, item):
        """ Add an item to the collection """
        if not isinstance(item, self.instance):
            raise ValueError(f"{item} is not instance of {self.instance}")
        index = getattr(item, self.index, None)
        if index == None:
            raise AttributeError(f"{self.index} of {item} is invalid")
        self[index] = item

    def remove(self, item):
        """ Remove item from collection """
        if isinstance(item, self.instance):
            if item in self.data:
                self.data.remove(item)
        else:
            item = self[item]
            if item in self.data:
                self.data.remove(item)

    def remove_if(self, **attrs):
        """ Remove items if meet attribute conditions """
        for i in range(len(self.data) - 1, -1, -1):
            if self.has_attrs(self.data[i], **attrs):
                del self.data[i]

    def first(self):
        """ Get the first item in the object """
        return self.data[0]

    def last(self):
        """ Get the last item in the object """
        return self.data[-1]

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

    def get(self, index):
        """ Find one item in collection by indexor """
        cond = lambda i: getattr(i, self.index, None) == index
        results = self.find(cond)
        return results[0] if len(results) > 0 else None

    def find(self, condition):
        """ Find all objects which meet callable condition """
        return [item for item in self if condition(item)]

    def find_by(self, **attrs):
        """ Find using arguments and attr to value filters """
        return self.find(lambda i: self.has_attrs(i, **attrs))
