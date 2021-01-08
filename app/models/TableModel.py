from app.models import PlaceModel, FileModel
from app.models.BaseModel import BaseModel
from tortoise import fields


class TableModel(BaseModel):
    class Meta:
        table = 'table'
        table_description = 'Represents table'

    place: fields.ForeignKeyRelation[PlaceModel] = fields.ForeignKeyField(model_name='models.PlaceModel',
                                                                          related_name='tables')
    name = fields.CharField(max_length=200)
    available = fields.BooleanField(default=True)
    capacity = fields.IntField()
    smoking = fields.BooleanField(default=False)
    description = fields.CharField(max_length=1000, default='')
    image: fields.ForeignKeyRelation[FileModel] = fields.ForeignKeyField(model_name='models.FileModel',
                                                                         related_name='table')
