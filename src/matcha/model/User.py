from matcha.orm.meta import Model, CharField, IntField

class User(Model):
    id = IntField()
    first_name = CharField()
    last_name = CharField()
    password = CharField()

    def __str__(self):
        if self.id is None:
            return "Null"
        else:
            return '(' + str(self.id) + ') ' + self.first_name + ' ' +self.last_name 
        