import importlib
import inspect
import dataclasses
from matcha.orm.meta import Field

def create_instance(class_str:str):
    """
    Create a class instance from a full path to a class constructor
    :param class_str: module name plus '.' plus class name and optional parents with arguments for the class's
        __init__() method. For example, "a.b.ClassB.ClassB('World')"
    :return: an instance of the class specified.
    """
    try:
        if "(" in class_str:
            full_class_name, args = class_name = class_str.rsplit('(', 1)
            args = '(' + args
        else:
            full_class_name = class_str
            args = ()
        # Get the class object
        module_path, _, class_name = full_class_name.rpartition('.')
        mod = importlib.import_module(module_path)
        klazz = getattr(mod, class_name)
        # Alias the the class so its constructor can be called, see the following link.
        # See https://www.programiz.com/python-programming/methods/built-in/eval
        alias = class_name + "Alias"
        instance = eval(alias + args, { alias: klazz})
        return instance
    except (ImportError, AttributeError):
        raise ImportError(class_str)

def find_class(class_str:str):
    """
    Create a class instance from a full path to a class constructor
    :param class_str: module name plus '.' plus class name and optional parents with arguments for the class's
        __init__() method. For example, "a.b.ClassB.ClassB('World')"
    :return: an instance of the class specified.
    """
    try:
        if "(" in class_str:
            full_class_name, args = class_name = class_str.rsplit('(', 1)
            args = '(' + args
        else:
            full_class_name = class_str
            args = ()
        # Get the class object
        module_path, _, class_name = full_class_name.rpartition('.')
        mod = importlib.import_module(module_path)
        klazz = getattr(mod, class_name)
        return klazz
    except (ImportError, AttributeError):
        raise ImportError(class_str)

def introspect(obj):
    for func in [type, id, dir, vars, callable]:
        print("%s(%s):\t\t%s" % (func.__name__, introspect.__code__.co_varnames[0], func(obj)))

def get_fields(cls_):
    fields = {}
    for key, val in cls_.__dict__.iteritems():
        if isinstance(val, Field):
            fields[key] = val
    return fields
    

if __name__ == "__main__":
    klazz = find_class("matcha.model.Users.Users()")
    print("Klazz:", klazz)
#     fields = get_fields(klazz)
#     print("Fiels:", fields)
    instance = create_instance("matcha.model.Users.Users()")
    print("Fields", dataclasses.fields(instance))
#    introspect(instance)

#     for member in inspect.getmembers(instance):
#         if not member[0].startswith('_') and not inspect.ismethod(member[1]):
#             print("Member:", member[0])

#     print("Dict:", instance.__dict__)
#     print("Instance:", instance)
#     instance.id = 1
#     instance.first_name = 'Pierre'
#     instance.last_name = 'Dupont' 
#     print("Instance:", instance)
#     print("Dict:", instance.__dict__)
#     