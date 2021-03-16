from matcha.orm.model_reflection import ModelDict
import psycopg2 as p

def quote(value, isnumeric):
    return value if isnumeric else "'" + str(value) + "'"

class Query():
    def __init__(self, model_name):
        self.model_name = model_name
    
    def get_query(self):
        query = "select "
        first = True
        model = ModelDict().get_model(self.model_name)
        for field in model.get_fields():
            query += (" " if first else ", ") + field.name
            first = False
        query += " from " + self.model_name
        return query
        

class DataAccess():
    __instance = None
    __modelDict = ModelDict()
    __connection = None
    
    def __new__(cls):
        if DataAccess.__instance is None:
            DataAccess.__instance = object.__new__(cls)
        return DataAccess.__instance

    @staticmethod
    def get_connection():
        if DataAccess.__connection is None:
            DataAccess.connection = p.connect(host="localhost", database="matchadb", user="matchaadmin", password="matchapass")
        return DataAccess.connection

    @staticmethod
    def fetch(model_name):
        query = Query(model_name).get_query()
        with DataAccess.get_connection().cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
#            for record in records:
                
            return records

    @staticmethod
    def merge(record):
        model_name = type(record).get_model_name()
        model = ModelDict().get_model(model_name)
        cmd = "update " + model_name
        
        for field in model.get_fields():
            val = getattr(record, field.name)
            print(field.name, ':', val)
        print("cmd:", cmd)

    @staticmethod
    def persist(record):
        pass

    @staticmethod
    def remove(record):
        pass