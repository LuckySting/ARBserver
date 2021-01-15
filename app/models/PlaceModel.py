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
    work_time_start = fields.CharField(default='', max_length=5, description='Place work time start')
    work_time_stop = fields.CharField(default='', max_length=5, description='Place work time start')
    preorder = fields.BooleanField(default=False, description='Preorder is allowed')
    tables: fields.ReverseRelation["TableModel"]
    rating = fields.IntField(description='Rating of the place', default=25)
    min_intervals_for_book = fields.IntField(description='Min number of intervals of 30 min for booking', default=1)
    max_intervals_for_book = fields.IntField(description='Max number of intervals of 30 min for booking', default=10)


class PlaceGallery(Model):
    place: fields.ForeignKeyRelation[PlaceModel] = fields.ForeignKeyField(model_name='models.PlaceModel',
                                                                          related_name='gallery')
    file: fields.ForeignKeyRelation[FileModel] = fields.ForeignKeyField(model_name='models.FileModel')
