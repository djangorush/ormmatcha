from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, CharField, IntField, DateField, DateTimeField, EmailField, BoolField, EnumField, TextField,\
    OneToManyField, ManyToManyField

@dataclass(init=False)
class Users(ModelObject):
    id: IntField(iskey=True)
    first_name: CharField(length=45)
    last_name: CharField(length=45)
    user_name: CharField(length=45)
    password: CharField(length=45)
    description: TextField()
    email: EmailField()
    active: BoolField()
    confirm: CharField(length=20)
    gender: EnumField(values=['Male', 'Female'])
    orientation: EnumField(values=['Hetero', 'Homo', 'bi'])
    birthday: DateField()
    last_update: DateTimeField(iscomputed=True)
    tags: ManyToManyField(jointable='users_tag', modelname='Tag', keyfieldname='users_id', joinfieldname='id')
    connections: OneToManyField(modelname='Connection', keyfieldname='users_id')