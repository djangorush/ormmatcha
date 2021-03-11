'''
Created on Mar 10, 2021

@author: yde-mont
'''

import inspect
from matcha.orm.meta import MetaModel
from matcha.model.User import User

class Test:
    def __init__(self):
        self.title = ""
        self.id = -1

def introspect(obj):
    for func in [type, id, dir, vars, callable]:
        print("%s(%s):\t\t%s" % (func.__name__, introspect.__code__.co_varnames[0], func(obj)))

def is_field(attr):
    print("attr", attr, "Type:", type(attr))
    return False

if __name__ == '__main__':
    print("toto")
    toto = inspect.getmembers(User(), lambda attr: is_field(attr))
    print("class:", type(toto))
    for i in toto:
        print('i:', i, 'i[0]:', i[0], 'Type:', type(i))
    for i in User().__dict__:
        print('i:', i, 'i[0]:', i[0], 'Type:', type(i))

