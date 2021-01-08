from app.models.BaseModel import BaseModel
from tortoise import fields


class PlaceModel(BaseModel):
    class Meta:
        table = 'place'

    restaurant = fields.ForeignKeyField(model_name='models.RestaurantModel', related_name='places')
