import psycopg2 as p
from matcha.orm.reflection import ModelDict
import matcha.config
import logging
from matcha.orm.reflection import OneToManyField, ManyToManyField

class Query():
    """
    Class Query for buildinq a sql command from parameters list
    """
    def __init__(self, model, leftjoins, conditions, whereaddon, orderby):
        self.model = model
        self.leftjoins = leftjoins
        self.conditions = conditions
        self.orderby = orderby
        self.whereaddon = whereaddon
    
    """
    Append member to value whith prefix, returning value
        if current value equal None append firstprefix otherwise otherprefix, then concatenate member  
    """
    def append(self, value, member, firstprefix, otherprefix):
        if value is None:
            return firstprefix + member
        else:
            return value + otherprefix + member

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
        parameters = tuple()
        for condition in conditions:
            fcondition = self.get_condition(condition)
            member = fcondition[0] + fcondition[1] + '%s'
            parameters += (fcondition[2],)
            where = self.append(where, member, " where ", " and ")
        return where, parameters
    
    """
    Build query
        - return query string and tuple of parameters
    """
    def build_query(self):
        model_name  = self.model.name
        self.suffix = model_name[0]
        query = "select "
        from_clause = " from " + self.model.name + ' ' + self.suffix
        first = True
        model = ModelDict().get_model(model_name)
        for field in model.get_fields():
            if not isinstance(field.type, OneToManyField):
                query += (" " if first else ", ") + self.suffix + '.' + field.name
                first = False
        """
        leftjoin--> 0:fieldName, 1:suffix, 2:join model, 3:ManyToOne field 
        """
        for leftjoin in self.leftjoins:
            field = leftjoin[3]          
            from_clause += " left outer join " + field.type.modelname + ' ' + leftjoin[1]
            for field in leftjoin[2].get_fields():
                if not isinstance(field.type, OneToManyField):
                    query += ", " + leftjoin[1] + '.' + field.name
                    if field.type.iskey:
                        from_clause += " on " +self.suffix + '.' + leftjoin[0] + ' = ' + leftjoin[1] + '.' + field.name
        query += from_clause
        where_clause, parameters = self.build_where(self.conditions)
        if not self.whereaddon is None:
            where_clause = self.append(where_clause, self.whereaddon[0], " where ", " and ")
            size = len(self.whereaddon)
            for i in range(1,size):
                parameters += (self.whereaddon[i],)
        if not where_clause is None:
            query += where_clause
        if not self.orderby is None:
            query += ' order by ' + self.orderby
        logging.debug("query:" + query)
        return query, parameters

"""
    Class DataAccess
    ----------------
"""
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
    
    """
    Check for singleton
    """
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
            if not isinstance(field.type, OneToManyField):
                setattr(modelobject,field.name,record[i])
                i += 1
        return (modelobject, i)
    
    def get_set_elements(self, suffix, _id, setjoin):
        """
        setjoin--> 0:fieldName, 1:suffix, 2:join model, 3:ManyToOne field 
        """
        objects = []
        fieldtype = setjoin[3].type
        if isinstance(setjoin[3].type, ManyToManyField):
            setmodel = ModelDict().get_model(setjoin[3].type.modelname)
            addonclause = "exists ( select 1 from " + fieldtype.jointable + " xyz where " + suffix + "." + fieldtype.joinfieldname + " = xyz." + fieldtype.keyfieldname + ")"
            records = self.__fetch_records(setmodel, leftjoins=[], conditions=[], whereaddon=(addonclause, ), orderby=fieldtype.orderby)
        else:
            records = self.__fetch_records(setjoin[2], leftjoins=[], conditions=(fieldtype.keyfieldname, _id), whereaddon=None, orderby=fieldtype.orderby)
        for record in records:
            (modelobject, _) = self.populate(record, setjoin[2], 0)
            objects.append(modelobject)
        return objects

    def __fetch_records(self, model, leftjoins, conditions, whereaddon, orderby):
        query, parameters = Query(model, leftjoins, conditions, whereaddon, orderby).build_query()
        with DataAccess.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            records = cursor.fetchall()
            return records

    def fetch(self, model_name, joins=[], conditions=[], whereaddon=None, orderby=None):
        model = ModelDict().get_model(model_name)
        objects = []
        """
        leftjoin--> 0:fieldName, 1:suffix, 2:join model, 3:ManyToOne field 
        """
        leftjoins = [] 
        setjoins = [] 
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
            if not isinstance(joinfield.type, OneToManyField):
                leftjoins.append(leftjoin)
            else:
                setjoins.append(leftjoin)
        records = self.__fetch_records(model, leftjoins, conditions, whereaddon, orderby)
        for record in records:
            (modelobject, start) = self.populate(record, model, 0)
            objects.append(modelobject)
            for leftjoin in leftjoins:
                (joinobject, start) = self.populate(record, leftjoin[2], start)
                setattr(modelobject,leftjoin[0],joinobject)
            for setjoin in setjoins:
                _id = getattr(modelobject, model.get_key_field().name)
                setattr(modelobject, setjoin[0], self.get_set_elements(suffix, _id, setjoin))
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
        
    def execute(self, cmd, parameters=None, model=None, record=None):
        with DataAccess.__connection.cursor() as cursor:
            cursor.execute(cmd, parameters)
            if not record is None:
                updatedrecord = cursor.fetchone()
                i = 0
                for field in model.get_fields():
                    if field.type.iskey or field.type.iscomputed:
                        setattr(record,field.name,updatedrecord[i])
                    i += 1
                returnvalue = record
            else:
                returnvalue = None
            DataAccess.__connection.commit()
            logging.debug("Excecute:" + cmd)
            return returnvalue
        
    def merge(self, record):
        model, model_name = self.getModel(record)
        cmd = "update " + model_name + " set"
        addon = ' '
        parameters = tuple()
        for field in model.get_fields():
            if not field.type.iskey and not field.type.iscomputed and not isinstance(field.type, OneToManyField):
                cmd += addon + field.name + " = %s"
                addon = ', '
                parameters += (getattr(record, field.name),)
            elif 'last_update' == field.name and field.type.iscomputed:
                cmd += addon + "last_update = DEFAULT"
        key_field = model.get_key_field().name
        cmd += ' where ' +  key_field + ' = ' + str(getattr(record, key_field)) + ' returning *'
        self.execute(cmd, parameters, model, record)
                   
    def persist(self, record):
        model, model_name = self.getModel(record)
        cmd = "insert into " + model_name
        columns = ''
        values = ''
        addon = '('
        parameters = tuple()
        for field in model.get_fields():
            if not field.type.iskey and not field.type.iscomputed and not isinstance(field.type, OneToManyField):
                columns += addon + field.name
                values += addon + '%s'
                parameters += (getattr(record, field.name), )
                addon = ', '
        cmd += columns + ') values ' + values + ') returning *'
        self.execute(cmd, parameters, model, record)

    def remove(self, record):
        model, model_name = self.getModel(record)
        key_field = model.get_key_field().name
        cmd = 'delete from ' + model_name + ' where ' +  key_field + ' = ' + str(getattr(record, key_field)) + " returning *"
        self.execute(cmd)
        
