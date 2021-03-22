from datetime import datetime

def append_where(where, clause):
    if where is None:
        where = " where "
    else:
        where += " and "
    where = where + clause
    return where

if __name__ == "__main__":
    t = datetime(2021, 3, 17, 10, 1, 30)
    print("t:", t)
    
    date_time_str = '18/09/19 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
    print(date_time_obj)
    where1 = append_where(None, "id = 1")
    where2 = append_where(where1, "id = 2")
    print(where1, ", ", where2)

    tu = (1, (2, 4), 3)
    for t in tu:
        print("Type:", type(t), "Value:", t)
        
    ti = (tu)
    print("oops", ti[0])
    
    
    l1 = [1,2,3]
    i = 3
    
    b1 = (type(l1) is list)
    b2 = (type(i) is list)
    print("Res:", b1, b2)    