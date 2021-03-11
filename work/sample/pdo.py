"""###############################################################
#  PDO:Python Database Objects - Version 1.3.2                #
###############################################################
#  info@neurokode.com                                         #
###############################################################
#  Copyright (c) 2003, NeuroKode Labs, All rights reserved.   #
#  Redistribution and use in source and binary forms, with    #
#  or without modification, are permitted provided that the   #
#  following conditions are met:                              #
#                                                             #
#  Redistributions of source code must retain the above       #
#  copyright notice, this list of conditions and the          #
#  following disclaimer.                                      #
#  Redistributions in binary form must reproduce the above    #
#  copyright notice, this list of conditions and the          #
#  following disclaimer in the documentation and/or other     #
#  materials provided with the distribution.                  #
#  Neither the name of NeuroKode Labs nor the names of its    #
#  contributors may be used to endorse or promote products    #
#  derived from this software without specific prior          #
#  written permission.                                        #
#                                                             #
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND     #
#  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED            #
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED     #
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A            #
#  PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE   #
#  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,  #
#  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL #
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF     #
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR        #
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON   #
#  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT       #
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)     #
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN   #
#  IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              #
###############################################################
# Supports:                                                   #
#     MySQLdb                                                 #
#     PySQLite                                                #
#     SQLite                                                  #
#     kinterbasedb                                            #
#     mxODBC                                                  #
#     DB2                                                     #
#     cx_Oracle                                               #
#     adodbapi                                                #
#     psycopg                                                 #
###############################################################"""

import string
import sys

class connect:
    def __init__(self, raw_connect_string):
        #Declare instance level variables for later comparisons:
        self.__module=""
        self.__connection_vars={}
        self.active=""
        self.PDODB=""
        con_required = {}
        con_defaults = {}
        con_rename = {}
        
        #Set Up: Parse the incomming connection string.
        connection_item_list = string.split(raw_connect_string, ";")
        for a in connection_item_list:
            if len(a) > 3:  # if incomplete fragment, skip
                b = string.split(a,"=")
                if string.lower(b[0])=="module":
                    self.__module = b[1]
                    self.module = b[1]
                    try:
                        self.PDODB = __import__(b[1],globals(),locals(),['connect'])
                        self.paramstyle = self.PDODB.paramstyle
                        self.last_paramark = 0   # user for numeric param markers in queries
                    except:
                        # you get here if ANY error occurs
                        self.active = 0
                        self.ErrorMessage="Unable to load Database Module: Database specific Error:" + str(sys.exc_type) + "\n" + str(sys.exc_value)
                        raise pdo_connection_error, self.ErrorMessage
                else:
                    if len(b) < 2:
                        b.append("")  # empty value
                    self.__connection_vars[string.lower(b[0])]=b[1]
                    
        #Validation: Setup
        con_required['MySQLdb'] = ['host','port','user','passwd','db']
        con_required['pgdb'] = ['user','password','database']
        con_required['sqlite'] = ['db']
        con_required['kinterbasdb'] = ['dsn', 'user', 'password']
        con_required['mx.ODBC.Windows'] = ['dsn', 'user', 'password']
        con_required['mx.ODBC.iODBC'] = ['dsn', 'user', 'password']
        con_required['mx.ODBC.unixODBC'] = ['dsn', 'user', 'password']
        con_required['DB2'] = ['dsn', 'user', 'password']
        con_required['cx_Oracle'] = ['dsn', 'user', 'password', 'mode']
        con_required['adodbapi'] = []
        con_required['psycopg'] = ['user','password','database']
        
        con_defaults['MySQLdb'] = {}
        con_defaults['MySQLdb']['host'] = 'localhost'
        con_defaults['MySQLdb']['port'] = 3306
        con_defaults['pgdb'] = {}
        con_defaults['sqlite'] = {}
        con_defaults['kinterbasdb'] = {}
        con_defaults['mx.ODBC.Windows'] = {}
        con_defaults['mx.ODBC.iODBC'] = {}
        con_defaults['mx.ODBC.unixODBC'] = {}
        con_defaults['DB2'] = {}
        con_defaults['adodbapi'] = {}
        con_defaults['cx_Oracle'] = {}
        con_defaults['cx_Oracle']['mode'] = 0
        con_defaults['psycopg']={}
        
        con_rename['MySQLdb'] = {}
        con_rename['MySQLdb']['password'] = "passwd"
        con_rename['pgdb'] = {}
        con_rename['DB2'] = {}
        con_rename['adodbapi'] = {}
        con_rename['pgdb']['passwd'] = "password"
        con_rename['pgdb']['db'] = "database"
        con_rename['sqlite'] = {}
        con_rename['kinterbasdb'] = {}
        con_rename['kinterbasdb']['passwd'] = "password"
        con_rename['mx.ODBC.Windows'] = {}
        con_rename['mx.ODBC.Windows']['passwd'] = "password"
        con_rename['mx.ODBC.iODBC'] = {}
        con_rename['mx.ODBC.iODBC']['passwd'] = "password"
        con_rename['mx.ODBC.unixODBC'] = {}
        con_rename['mx.ODBC.unixODBC']['passwd'] = "password"
        con_rename['DB2']['passwd'] = "pwd"
        con_rename['DB2']['user'] = "uid"
        con_rename['cx_Oracle'] = {}
        con_rename['cx_Oracle']['passwd'] = "password"
        con_rename['psycopg']={}
        con_rename['psycopg']['passwd'] = "password"
        con_rename['psycopg']['dbname'] = "database"
        
        #Validation: Rename any fields from pdo-name to db-specific name.
        for myKey in con_rename[self.__module].keys():
            if self.__connection_vars.has_key(myKey):
                self.__connection_vars[con_rename[self.__module][myKey]]=self.__connection_vars[myKey]
                del self.__connection_vars[myKey]

        #Validation: Now set any missing fields to defaults.
        for myKey in con_defaults[self.__module].keys():
            if not self.__connection_vars.has_key(myKey):
                self.__connection_vars[myKey] = con_defaults[self.__module][myKey]

        #Validation: Now make sure we have the required fields.
        any_missing = []
        for item in con_required[self.__module]:
            if not self.__connection_vars.has_key(item):
                any_missing.append(item)
                
        #Validation: Supported Module
        if not con_required.has_key(self.__module):
            self.active=0
            raise pdo_connection_error, "Unsupported DB-API Module."
        
        #print self.__connection_vars.keys()
        #Connection: Try the connection or raise an Error Message
        try:
            #EXCEPTION: Check the module to see if the user is trying to connect through the
            #cx_Oracle Module. If they are use Non-Keywords based Connection String.
            if self.module=="cx_Oracle":
                self.db = self.PDODB.connect(self.__connection_vars['user'], self.__connection_vars['password'], self.__connection_vars['dsn'], int(self.__connection_vars['mode']))
            elif self.module=="adodbapi":
                # rebuild the connection string, everything except module is input
                con_str = ""
                for item in self.__connection_vars.keys():
                    con_str += item + "=" + self.__connection_vars[item] + ";"
                self.db = self.PDODB.connect(con_str)
            else:
                self.db = self.PDODB.connect(**self.__connection_vars)
            self.active=1
           
        except:
            self.active=0
            raise pdo_connection_error, "Unable to connect to the Database: Database specific Error:" + str(sys.exc_type) + "\n" + str(sys.exc_value)

    def close(self):
        try:
            self.db.close()
            self.active=0
            
        except:
            raise pdo_connection_error, "Unable to close connection to the Database:  Database specific Error: " + str(sys.exc_type) + "\n" + str(sys.exc_value)
    
    
    def openRS(self, sql_statement):
        #Depricated: Use connection.open()
        self.rs = resultsource(self, sql_statement)
        return self.rs
        
    def open(self, sql_statement="", Params=None):
        self.rs = resultsource(self, sql_statement, Params)
        return self.rs

    def simpleCMD(self, sql_statement):
        #Depricated: use .execute()
        self.se = SimpleExecute(self, sql_statement)
        return self.se
        
    def pmark(self):
        if self.paramstyle == 'qmark':
            return "?"
        elif self.paramstyle == 'numeric':
            self.last_paramark += 1
            return ":" + str(self.last_paramark) 
        else: 
          
            raise pdo_pmark_error, "pdo_pmark_error: Invalid use of pmark(): the current paramstyle is not qmark(?) or numeric(:1)."  
        
    def execute(self, sql_statement="", paramlist=None):
        if paramlist == None:
            self.se = SimpleExecute(self, sql_statement)
        else:
            self.se = ParamExecute(self, sql_statement, paramlist)
        self.last_paramark = 0
        return self.se
        
    def execute_many(self, sql_statement, paramlist):
        self.se = ParamExecuteMulti(self, sql_statement, paramlist)
        self.last_paramark = 0
        return self.se
        
    def get_cursor(self):
        self.cursor=self.db.cursor()
        return self.cursor


class resultsource:
    def __init__(self, parent, select_statement="", Params=None):
        #Variable Declaration
        self.__cursor = parent.db.cursor()
        self.fields={}
                
        #Run the statement: Append an Error Message to the Instances Error String. 
        try:
            if Params == None:
                self.__cursor.execute(select_statement)
            else:
                self.__cursor.execute(select_statement, Params)
        except:
            raise pdo_resultset_error, "ResultSet Error: Database specific Error:" + str(sys.exc_type) + "\n" + str(sys.exc_value)
            
        #With a Valid RecordSet, bring the entire Recordset into Memory.
        #Set Our Cursor Point at the First Record of the First Row.     
        try:
            self.__rs = self.__cursor.fetchall()
            self.__row = -1
            self.__column = 0
            tmp_position=0
            for i in self.__cursor.description:
                self.fields[i[0]] = Field(i[0], i[1], i[2], i[3], i[4], i[5], i[6], tmp_position, self.__row, self.__rs)
                tmp_position = tmp_position + 1    
        except:
            raise pdo_resultset_error, "ResultSet Error: Database specific Error:" + str(sys.exc_type) + "\n" + str(sys.exc_value)

    def close(self):
        self.__cursor.close()
        self.__rs = None
        for field in self.fields.keys():
            self.fields[field].rows = None
            self.fields[field].cur_row = None
            del self.fields[field]
        #del self
    
    def __getitem__(self, Args=None):
        k = self.fields[Args]
        return k

    def __contains__(self, Args):
        return has_key(Args)

    def __setitem__(self):
        raise NotImplementedError, "This option is not supported"

    def keys(self, L=[]):
        L= None
        L = []
        for i in self.fields:
            L.append(i)
        return L

    def has_key(self, Args):
        if self.fields.has_key(Args):
            return 1
        else:
            return 0

    def get_cur_val(self, column):
        row = self.__row
        k = self.__rs[row][column]
        return k
        
    def row_count(self):
        return len(self.__rs)

    def first(self):
        #Return the first row of the result set.
        self.__row=0
        return 1

    def last(self):
        #Return the Last row of the result set.
        self.__row = len(self.__rs)-1
        return 1

    def reset_field_positions(self):
        for field in self.fields.keys():
            self.fields[field].cur_row = self.__row 

    def next(self):
        if self.__row==-1:
            current_position=0
        else:
            current_position = self.__row + 1
        
        row_count = len(self.__rs)

        result = 1
        if current_position==row_count:
            result = 0
        else:
            self.__row = current_position
            result =  1
        self.reset_field_positions()    
        return result    
    

    def prev(self):
        if self.__row==-1:
            current_position = 0
        else:
            current_position = self.__row - 1
        
        result = 1
        if self.__row==0:
            result = 0
        else:
            self.__row = current_position
            result = 1

        self.reset_field_positions()    
        return result

    def move(self, move_row):
        destination_row=self.__row + move_row
        row_count=len(self.__rs)
        
        result = 1
        if destination_row < 0 or destination_row > row_count:
            result = 0
        else:
            self.__row=destination_row
            result = 1

        self.reset_field_positions()    
        return result

    def moveto(self, move_row):
        row_count=len(self.__rs)
        if move_row < 0:
            start_row=row_count
        else:
            start_row=0
        destination_row=start_row+move_row
        
        result = 1
        if destination_row > row_count or destination_row < 0:
            result = 0
        else:
            self.__row=destination_row
            result = 1

        self.reset_field_positions()
        return result

    def array_from_column(self, column_name):
        self.cur_arr=[]
        current_row=self.__row
        self.__row=-1
        self.reset_field_positions()

        while self.next():
            self.cur_arr.append(self.fields[column_name].value)
        self.__row=current_row
        self.reset_field_positions()
        return self.cur_arr
        
    def dictionary_from_columns(self, column_key, column_value):
        self.cur_dict={}
        current_row=self.__row
        self.__row=-1
        self.reset_field_positions()

        while self.next():
            self.cur_dict[self.fields[column_key].value]=self.fields[column_value].value

        self.reset_field_positions()
        self.__row=current_row
        return self.cur_dict

    def reset(self):
        self.__row=-1
        return 1

class Field:
    #Field Object. Returns information about the specified field.
    #Based upon DB-API 2.0 cursor.description:
    # name, type_code,display_size, internal_size, precision, scale,null_ok 
    def  __init__(self, fname, ftype, defined_size, internal_size, precision, scale, null_ok, position, current_row, rows_list):
        self.name = fname
        self.type_id = ftype
        self.size = defined_size
        self.length = internal_size
        self.precision = precision
        self.scale = scale
        self.null_ok = null_ok
        self.position = position
        self.cur_row = current_row
        self.rows = rows_list

    def __getattr__(self, name):
        if (name=="value"):
            return self.get_cur_val(self.position)
            
    def get_cur_val(self, position):
        row = self.cur_row
        k = self.rows[row][position]
        return k
            
            

class ParamExecute:
    def __init__(self, parent, Statement, Params):
        self.__cursor = parent.db.cursor()
        try:
            self.affected_rows = self.__cursor.execute(Statement, Params)
        except:
            raise pdo_param_execute_error, "Paramater-enabled Execute Error: Database specific Error:" + str(sys.exc_type) + "\n" + str(sys.exc_value)
            self.affected_rows = 0

class ParamExecuteMulti:     # same as above, but calls executemany
    def __init__(self, parent, Statement, Params):
        self.__cursor = parent.db.cursor()
        try:
            self.affected_rows = self.__cursor.executemany(Statement, Params)
            
        except:
            raise pdo_param_execute_error, "Paramater-enabled ExecuteMany Error: Database specific Error:" + str(sys.exc_type) + "\n" + str(sys.exc_value)
            self.affected_rows = 0
            
class SimpleExecute:
    def __init__(self, parent, Statement):
        self.__cursor = parent.db.cursor()
        try:
            self.affected_rows = self.__cursor.execute(Statement)
            try:
                self.insertid=self.__cursor.lastrowid
            except:
                self.insertid = None                
        except:
            raise pdo_simple_execute_error, "Simple Execute Error: Database specific Error:" + str(sys.exc_type) + "\n" + str(sys.exc_value)
            self.affected_rows = 0

class pdo_pmark_error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
            
class pdo_connection_error(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)

class pdo_resultset_error(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)
        
class pdo_simple_execute_error(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)                                                                                                                                                                                                                                                                       

class pdo_param_execute_error(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)
