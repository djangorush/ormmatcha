from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, ManyToOneField, IntField, DateTimeField, TextField

@dataclass(init=False)
class Users(ModelObject):
    id: IntField(iskey=True)
    users_id1: ManyToOneField(modelname='Users')
    users_id1: ManyToOneField(modelname='Users')
    chat: TextField()
    last_update: DateTimeField(iscomputed=True)