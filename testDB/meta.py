from matcha.orm.model_reflection import ModelDict
from datetime import datetime
import re

class Field:
    
    def __init__(self, iscomputed=False, iskey=False, isnumeric=False):
        self.value = None
        self.iscomputed = iscomputed
        self.iskey = iskey
        self.isnumeric = isnumeric
    
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = value

class IntField(Field):

    def __init__(self, iscomputed=False, iskey=False, isnumeric=True):
        Field.__init__(self, iscomputed, iskey, isnumeric)
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(instance, self._name, int, value)
        super().__set__(instance, value)

class CharField(Field):
    def __init__(self, iscomputed=False, iskey=False, isnumeric=False, length=None):
        Field.__init__(self, iscomputed, iskey, isnumeric)
        self.length = length
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        if len(value) > self.length:
            raise ValueError("Maximum length('"+ self.length + ") is exceeded by value '" + value + "'!")
        super().__set__(instance, value)

class TextField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        super().__set__(instance, value)

class EmailField(Field):
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        if not re.search("'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'", value):
            raise ValueError("''" + "is not a valid email!")
        super().__set__(instance, value)

class EnumField(Field):

    def __init__(self, iscomputed=False, iskey=False, isnumeric=False, values=[]):
        Field.__init__(self, iscomputed, iskey, isnumeric)
        self.values = values
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(instance, self._name, int, value)
        if value not in self.values:
            raise ValueError("'" + value + "' is not a authorized value for enum '"+ self.values + "'!'" )
        super().__set__(instance, value)

class BoolField(Field):

    def __init__(self, iscomputed=False, iskey=False, isnumeric=True):
        Field.__init__(self, iscomputed, iskey, isnumeric)
    
    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise TypeError(instance, self._name, bool, value)
        super().__set__(instance, value)

class DateField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, datetime):
            raise TypeError(instance, self._name, datetime, value)
        super().__set__(instance, datetime.datetime(value.year, value.month, value.day))

class DateTimeField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, datetime):
            raise TypeError(instance, self._name, datetime, value)
        super().__set__(instance, value)

class ImageField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        if len(value) > 255:
            raise ValueError("Maximum length('"+ self.length + ") is exceeded by value '" + value + "'!")
        super().__set__(instance, value)

class ManyToOneField(Field):
    def __init__(self, modelname=None, iscomputed=False, iskey=False, isnumeric=False):
        Field.__init__(self, iscomputed, iskey, isnumeric)
        self.modelname = modelname
        self.model_value = None
    def __set__(self, instance, value):
        self.value = value

class ModelObject(object):
    @classmethod
    def get_model_name(cls):
        return cls.__name__
    
    def __str__(self):
        if self.id is None:
            return ModelObject.get_model_name() + " is None"
        else:
            model = ModelDict().get_model(self.get_model_name())
            return model.model_str(self) 
