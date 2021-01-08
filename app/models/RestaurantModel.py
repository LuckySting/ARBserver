from app.models.BaseModel import BaseModel
from tortoise import fields
from app.models.FileModel import FileModel


class RestaurantModel(BaseModel):
    class Meta:
        table = 'restaurant'
        table_description = 'Represents restaurant'

    name = fields.CharField(max_length=50, description='Name of the restaurant')
    description = fields.TextField(default='', description='Description of the restaurant')
    confirmed = fields.BooleanField(default=False, description='Is restaurant is validated by moderator')
    image: fields.ForeignKeyRelation[FileModel] = fields.ForeignKeyField(model_name='models.FileModel',
                                                                         related_name='restaurant')
    menu: fields.ReverseRelation["DishModel"]
    places: fields.ReverseRelation["PlaceModel"]
