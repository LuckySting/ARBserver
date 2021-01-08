from app.models import RestaurantModel
from app.models.BaseModel import BaseModel
from tortoise import fields, Model
from app.models.FileModel import FileModel


class PlaceModel(BaseModel):
    class Meta:
        table = 'place'
        table_description = 'Represents place'

    restaurant: fields.ForeignKeyRelation[RestaurantModel] = fields.ForeignKeyField(model_name='models.RestaurantModel',
                                                                                    related_name='places')
    address = fields.CharField(max_length=300, description='Address of the place')
    longitude = fields.FloatField(description='Longitude of the place')
    latitude = fields.FloatField(description='Latitude of the place')
    gallery: fields.ReverseRelation["PlaceGallery"]
    work_time = fields.CharField(max_length=100, description='Place work time')
    preorder = fields.BooleanField(default=False, description='Preorder is allowed')
    tables: fields.ReverseRelation["TableModel"]


class PlaceGallery(Model):
    place: fields.ForeignKeyRelation[PlaceModel] = fields.ForeignKeyField(model_name='models.PlaceModel',
                                                                          related_name='gallery')
    file: fields.ForeignKeyRelation[FileModel] = fields.ForeignKeyField(model_name='models.FileModel')
