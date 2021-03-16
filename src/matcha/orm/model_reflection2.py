import importlib
import dataclasses

def create_instance(class_name:str):
    """
    Create a class instance from class '{class_name}' from module 'matcha.model.{class_name}'
    """
    try:
        module_path = "matcha.model." + class_name
        mod = importlib.import_module(module_path)
        klazz = getattr(mod, class_name)
        # Alias the the class so its constructor can be called, see the following link.
        # See https://www.programiz.com/python-programming/methods/built-in/eval
        alias = class_name + "Alias"
        instance = eval(alias + "()", { alias: klazz})
        return instance
    except (ImportError, AttributeError):
        raise ImportError(class_name)

class TableModel():
    def __init__(self, instance):
        self.fields = []
        for field in dataclasses.fields(instance):
            self.fields.append(field)
    
    def get_fields(self):
        return self.fields;

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

    @classmethod
    def get_class(model_name:str):
        """
        Create a class instance from class '{class_name}' from module 'matcha.model.{class_name}'
        """
        try:
            module_path = "matcha.model." + model_name
            mod = importlib.import_module(module_path)
            return getattr(mod, model_name)
        except (ImportError, AttributeError):
            raise ImportError(model_name)
    @classmethod
    def get_instance(class_name:str):
        klazz = ModelDict.get_class(class_name)
        alias = class_name + "Alias"
        instance = eval(alias + "()", { alias: klazz})
        return instance
        
    def get_model(self, model_name:str):
        try:
            model = ModelDict.__models[model_name]
        except (KeyError):
            instance = ModelDict.get_instance(model_name) 
            model = TableModel(instance)
            ModelDict.__models[model_name] = model
        return model
    