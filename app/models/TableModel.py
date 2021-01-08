from app.models import PlaceModel
from app.models.BaseModel import BaseModel
from tortoise import fields


class TableModel(BaseModel):
    class Meta:
        table = 'table'
        table_description = 'Represents table'

    place: fields.ForeignKeyRelation[PlaceModel] = fields.ForeignKeyField(model_name='models.PlaceModel')
