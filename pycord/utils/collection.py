


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
            return key in self.values()
        for item in self.values():
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
        try:
            return next(filter(lambda x: x.id == id, self.values()))
        except StopIteration:
            return

        attrs['id'] = id or attrs.get('id')
        return self.find_one(lambda i: self.has_attrs(i, **attrs))
