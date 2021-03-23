from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from datetime import datetime
import logging

def append_where(where, clause):
    if where is None:
        where = " where "
    else:
        where += " and "
    where = where + clause
    return where

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    t = datetime(2021, 3, 17, 10, 1, 30)
    print("t:", t)
    
    date_time_str = '18/09/19 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
    print(date_time_obj)
    where1 = append_where(None, "id = 1")
    where2 = append_where(where1, "id = 2")
    print(where1, ", ", where2)

#     tu = (1, (2, 4), 3)
#     for t in tu:
#         print("Type:", type(t), "Value:", t)
#         
#     ti = (tu)
#     print("oops", ti[0])
#     
#     
#     l1 = [1,2,3]
#     i = 3
#     
#     b1 = (type(l1) is list)
#     b2 = (type(i) is list)
#     print("Res:", b1, b2)
#     
# 
#     t = tuple()
#     t = t +(1,)
#     t = t +(2,)
#     t = t +(3,)
#     t = t +(4,)
#     print(t)

    '''
    select Users 1 with set of connections
    '''
    records = DataAccess().fetch('Users', joins=['connections', 'tags'], conditions='1')
    print(records[0])
    for connection in records[0].connections:
        print(connection)
    if records[0].tags:
        for tag in records[0].tags:
            print(tag)
    
