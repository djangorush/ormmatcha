from datetime import datetime
import re
import importlib
import dataclasses

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
    def __init__(self, iscomputed=False, iskey=False, isnumeric=False, modelname=None):
        Field.__init__(self, iscomputed, iskey, isnumeric)
        if modelname is None is None:
            raise ValueError("'modelname' attribute must be specified!")
        self.modelname = modelname
    def __set__(self, instance, value):
        self.value = value

class OneToManyField(Field):
    def __init__(self, iscomputed=False, iskey=False, isnumeric=False, modelname=None, keyfieldname=None, orderby=None):
        if modelname is None or keyfieldname is None:
            raise ValueError("'modelname' and 'keyfieldname' attributes must be specified!")
        Field.__init__(self, iscomputed, iskey, isnumeric)
        self.modelname = modelname
        self.keyfieldname=keyfieldname
        self.orderby = orderby
    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise TypeError(instance, self._name, list, value)
        self.value = value

class ManyToManyField(OneToManyField):
    def __init__(self, iscomputed=False, iskey=False, isnumeric=False, modelname=None, keyfieldname=None, jointable=None, joinfieldname=None):
        if jointable is None or joinfieldname is None:
            raise ValueError("'jointable' and 'keyfieldname' attributes must be specified!")
        OneToManyField.__init__(self, iscomputed, iskey, isnumeric, modelname, keyfieldname)
        self.jointable = jointable
        self.joinfieldname = joinfieldname

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

class Model():
    def __init__(self, model_name):
        self.fields = []
        self.dictfields = {}
        self.name = model_name
        self.klazz = self.get_class()
        self.ket_field = None
        instance = self.new_instance()
        for field in dataclasses.fields(instance):
            self.fields.append(field)
            self.dictfields[field.name] = field
    
    def get_fields(self):
        return self.fields;

    def get_key_field(self):
        for field in self.fields:
            if field.type.iskey:
                self.key_field = field
                break
        return self.key_field;

    def get_field(self, field_name):
        try:
            return self.dictfields[field_name]
        except KeyError:
            raise ValueError("No field '" + field_name + "' for '" +self.name + "'!'")

    def new_instance(self):
        return eval("modelObject()", { "modelObject": self.klazz})
        
    def get_class(self):
        """
        Create a class instance from class '{class_name}' from module 'matcha.model.{class_name}'
        """
        try:
            module_path = "matcha.model." + self.name
            mod = importlib.import_module(module_path)
            return getattr(mod, self.name)
        except (ImportError, AttributeError):
            raise ImportError(self.name)
    
    def head(self, instance, model_name):
        head = model_name + "("
        delim = ''
        for field in self.fields:
            if field.type.iskey:
                head += delim + field.name + ': ' + str(getattr(instance, field.name))
                delim = ', '
        head += ")" 
        return head
        
    def model_str(self, instance):
#         head = self.name + "("
#         delim = ''
#         for field in self.fields:
#             if field.type.iskey:
#                 head += delim + field.name + ': ' + str(getattr(instance, field.name))
#                 delim = ', '
#         head += ")\n"
        model_str = self.head(instance, self.name)  + "\n"
        for field in self.fields:
            if not field.type.iskey and not isinstance(field.type, OneToManyField):
                attr = getattr(instance, field.name)
                if hasattr(attr, 'get_model_name'):
                    attr = self.head(attr, type(attr).__name__)
                model_str += '    ' + field.name + ': ' + str(attr) + '\n'
        return model_str

class ModelDict(object):
    """
    ModelDict est une classe singleton contenant dictionnaire (en cache) la liste des Objects
    et pour chaque objet la liste des champs.
    """
    __instance = None
    __models = {}
    def __new__(cls):
        if ModelDict.__instance is None:
            ModelDict.__instance = object.__new__(cls)
        return ModelDict.__instance

    
    def get_model(self, model_name:str):
        try:
            model = ModelDict.__models[model_name]
        except (KeyError):
            model = Model(model_name)
            ModelDict.__models[model_name] = model
        return model
    