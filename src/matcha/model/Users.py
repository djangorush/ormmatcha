from dataclasses import dataclass
from matcha.orm.meta import Model, CharField, IntField

@dataclass(init=False)
class Users(Model):
    id: IntField(iskey=True)
    first_name: CharField()
    last_name: CharField()
    password: CharField()
    email: CharField(iscomputed=True)

    def __str__(self):
        if self.id is None:
            return "Null"
        else:
            return '(' + str(self.id) + ') ' + self.first_name + ' ' +self.last_name 
        