import types
from matcha.orm.meta import Field
import importlib


def get_fields(cls_):
    fields = {}
    for key, val in cls_.__dict__.iteritems():
        if isinstance(val, Field):
            fields[key] = val
    return fields
    
class Inspection:

    __schema_tables_dict__ = {}
    
    @staticmethod
    def get_model(tablename):
        try:
            model = Inspection.__schema_tables_dict__[tablename]
        except (KeyError):
            model = Model(tablename)
            Inspection.__schema_tables_dict__[tablename] = model
        return model
        
""" Plain Old Python Object see POJO in Java """
class Model:
    def __init__(self, tablename):
        self.cls_ = types.new_class(tablename);
        self.fields = get_fields(self.cls_)
    

if __name__ == '__main__':
    inspection = Inspection()
    mod = importlib.import_module("matcha.model.User")
    klazz = getattr(mod, "User")
    for key, val in klazz.__dict__.iteritems():
        if isinstance(val, Field):
            print("Field", key)

    a = eval("User")()
    user_model = Inspection.get_model("User")    
    print("toto:", user_model)