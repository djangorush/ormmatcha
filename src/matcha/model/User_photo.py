from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, ImageField, ManyToOneField

@dataclass(init=False)
class User_photo(ModelObject):
    users_id: ManyToOneField(iskey=True)
    photo1: ImageField()
    photo2: ImageField()
    photo3: ImageField()
    photo4: ImageField()
    photo5: ImageField()
