import psycopg2 as p
from matcha.orm.reflection import ModelDict
import matcha.config
import logging

"""
Add quote when necessary
"""
def quote(field, value):
    if value is None:
        return 'null'
    if not field.type.isnumeric:
        return "'" + str(value) +"'"
    return str(value)
    
class Query():
    """
    Class Query for buildin a sql command from parameters list
    """
    def __init__(self, model, leftjoins, conditions, orderby):
        self.model = model
        self.leftjoins = leftjoins
        self.conditions = conditions
        self.orderby = orderby
    
    """
    Append condition to where clause
    """
    def append_where(self, where, condition):
        if where is None:
            where = " where "
        else:
            where += " and "
        field = self.model.get_field(condition[0].rpartition('.')[-1])
        where = where + condition[0] + condition[1] + quote(field, str(condition[2]))
        return where

    """
    get formatted condition from raw condition
    """
    def get_condition(self, condition):
        if not type(condition) is tuple:
            condition = ((condition,))
        size = len(condition)
        if 3 != size:
            if 2 == size:
                condition = (condition[0], '=', condition[1])
            elif 1 == size: 
                condition = (self.suffix + '.' + self.model.get_key_field().name, '=',) + condition
            else:
                raise ValueError("Invalid condition:" + condition)
        return condition
    
    """
    Build where clause from conditions
    """
    def build_where(self, conditions):
        if conditions is None:
            return None
        if not type(conditions) is list:
            conditions = [conditions]
        where = None
        for condition in conditions:
            where = self.append_where(where, self.get_condition(condition))
        return where
    
    def build_query(self):
        model_name  = self.model.name
        self.suffix = model_name[0]
        query = "select "
        from_clause = " from " + self.model.name + ' ' + self.suffix
        first = True
        model = ModelDict().get_model(model_name)
        for field in model.get_fields():
            query += (" " if first else ", ") + self.suffix + '.' + field.name
            first = False
        for leftjoin in self.leftjoins:
            field = leftjoin[3]          
            from_clause += " left outer join " + field.type.modelname + ' ' + leftjoin[1]
            for field in leftjoin[2].get_fields():
                query += ", " + leftjoin[1] + '.' + field.name
                if field.type.iskey:
                    from_clause += " on " +self.suffix + '.' + leftjoin[0] + ' = ' + leftjoin[1] + '.' + field.name
        query += from_clause
        where_clause = self.build_where(self.conditions)
        if not where_clause is None:
            query += where_clause
        if not self.orderby is None:
            query += ' order by ' + self.orderby
        logging.debug("query:" + query)
        return query
    
class DataAccess():
    """
    Singleton DataAccess class provides:
        - get_connection ->    connection
        - populate:      ->    Populate model object from record of result set
        - fetch:         ->    fetch model object from database with jointures according to conditions and order by clause
        - merge:         ->    Update database object from model object
        - persist:       ->    Insert database object from model object
        - remove:        ->    Delete database object corresponding to model object
    """
    __instance = None
    __modelDict = ModelDict()
    __connection = None
    
    def __new__(cls):
        """
        if previous instance is null instantiate and connect to database, elsewhere return current instance        
        """
        if DataAccess.__instance is None:
            DataAccess.__instance = object.__new__(cls)
            postgresql = matcha.config.config['postgresql']
            DataAccess.__connection = p.connect(host=postgresql['host'], database=postgresql['database'], user=postgresql['user'], password=postgresql['password'])
        return DataAccess.__instance

    def populate(self, record, model, start):
        modelobject = model.new_instance()
        i = start
        for field in model.get_fields():
            setattr(modelobject,field.name,record[i])
            i += 1
        return (modelobject, i)
    
    def __fetch_records(self, model, leftjoins, conditions, orderby):
        query = Query(model, leftjoins, conditions, orderby).build_query()
        with DataAccess.__connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            return records

    def fetch(self, model_name, joins=[], conditions=[], orderby=None):
        model = ModelDict().get_model(model_name)
        objects = []
        """
        leftjoin--> 0:fieldName, 1:suffix, 2:join model, 3:ManyToOne field 
        """
        leftjoins = [] 
        if not type(joins) is list:
            joins = [joins]
        for join in joins:
            suffix = None
            if type(join) is tuple:
                join_name = join[0]
                suffix =  join[1]
            else:
                join_name = join
            if suffix is None:
                suffix = join_name[0].upper()
            joinModel = ModelDict().get_model(model.get_field(join_name).type.modelname)
            joinfield = model.get_field(join_name)          
            leftjoin = (join_name, suffix, joinModel, joinfield)
            leftjoins.append(leftjoin)
        records = self.__fetch_records(model, leftjoins, conditions, orderby)
        for record in records:
            (modelobject, start) = self.populate(record, model, 0)
            objects.append(modelobject)
            for leftjoin in leftjoins:
                (joinobject, start) = self.populate(record, leftjoin[2], start)
                setattr(modelobject,leftjoin[0],joinobject)
        return objects

    def find(self, model_name, joins=[], conditions=[], orderby=None):
        objects = self.fetch(model_name, joins, conditions, orderby)
        size = len(objects)
        if 1 != size:
            message = ' for model object ' + model_name
            if joins:
                message += ', joins=' + str(joins)
            if conditions:
                message += ', conditions='+ str(conditions)
            if 0 == size:
                logging.debug("No record found" + message + '.')
                return None
            else:
                logging.warning("Several records found ("+ str(len(objects)) + ")" + message + '.')           
        return objects[0]
        
    def getModel(self, record):
        model_name = type(record).get_model_name()
        return ModelDict().get_model(model_name), model_name
        
    def execute(self, cmd):
        with DataAccess.__connection.cursor() as cursor:
            cursor.execute(cmd)
            DataAccess.__connection.commit()
            logging.debug("Excecute:" + cmd)
        
    def merge(self, record):
        model, model_name = self.getModel(record)
        cmd = "update " + model_name + " set"
        
        addon = ' '
        for field in model.get_fields():
            if not field.type.iskey and not field.type.iscomputed:
                cmd += addon + field.name + " = " +  quote(field, getattr(record, field.name))
                addon = ', '
        key_field = model.get_key_field().name
        cmd += ' where ' +  key_field + ' = ' + str(getattr(record, key_field))
        self.execute(cmd)
                   
    def persist(self, record):
        model, model_name = self.getModel(record)
        cmd = "insert into " + model_name
        columns = ''
        values = ''
        addon = '('
        for field in model.get_fields():
            if not field.type.iskey and not field.type.iscomputed:
                columns += addon + field.name
                values += addon + quote(field, getattr(record, field.name))
                addon = ', '
        cmd += columns + ') values ' + values + ')'
        self.execute(cmd)
        record = find()

    def remove(self, record):
        model, model_name = self.getModel(record)
        key_field = model.get_key_field().name
        cmd = 'delete from ' + model_name + ' where ' +  key_field + ' = ' + str(getattr(record, key_field))
        self.execute(cmd)
