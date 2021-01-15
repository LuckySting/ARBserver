from app.models.FileModel import FileModel
from app.models.RestaurantModel import RestaurantModel
from app.models.BaseModel import BaseModel
from tortoise import fields


class DishModel(BaseModel):
    class Meta:
        table = 'dish'
        table_description = 'Represents dish'

    restaurant: fields.ForeignKeyRelation[RestaurantModel] = fields.ForeignKeyField(model_name='models.RestaurantModel',
                                                                                    related_name='menu')
    name = fields.CharField(max_length=200, description='Name of the dish')
    description = fields.TextField(default='', description='Description of the dish')
    image: fields.ForeignKeyRelation[FileModel] = fields.ForeignKeyField(model_name='models.FileModel', related_name='dish')
    price = fields.FloatField(description='Price of the dish')
    sale = fields.BooleanField(default=False, description='Is on sale')
    sale_price = fields.FloatField(default=0, description='Sale price of the dish')
