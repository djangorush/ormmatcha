import inspect

class Field:
    value = None
    
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = value

class IntField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(instance, self._name, int, value)
        super().__set__(instance, value)


class CharField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        super().__set__(instance, value)

class MetaModel(type):

    def __init__(cls):
        fields = {}
        for key, val in cls.__dict__.iteritems():
            if isinstance(val, Field):
                fields[key] = val
        cls.fields = fields

class Model():
    fields = {}    
    
    def is_field(self, attr):
        return attr.is_instance(Field)

    def get_fields(self):
        if 0 == self.fields.__len__():
            self.fields = inspect.getmembers(self, lambda attr: self.is_field(attr))
        return self.fields;

if __name__ == '__main__':    
    print("toto")