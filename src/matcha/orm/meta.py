class Field:
    
    def __init__(self, iscomputed=False, iskey=False):
        self.value = None
        self.isnumeric = False
        self.iscomputed = iscomputed
        self.iskey = iskey
    
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = value

class IntField(Field):

    def __init__(self, iscomputed=False, iskey=False):
        self.value = None
        self.isnumeric = True
        self.iscomputed = iscomputed
        self.iskey = iskey
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(instance, self._name, int, value)
        super().__set__(instance, value)


class CharField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        super().__set__(instance, value)

class Model(object):
    @classmethod
    def G(cls):
        return cls.__name__