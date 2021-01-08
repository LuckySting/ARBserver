from app.models.RestaurantModel import RestaurantModel
from app.models.BaseModel import BaseModel
from tortoise import fields


class DishModel(BaseModel):
    class Meta:
        table = 'dish'

    restaurant: fields.ForeignKeyRelation[RestaurantModel] = fields.ForeignKeyField(model_name='models.RestaurantModel',
                                                                                    related_name='menu')
