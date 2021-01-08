from tortoise.models import Model
from tortoise import fields


class BaseModel(Model):
    id = fields.IntField(pk=True, description='Identifier field')
    created_at = fields.DatetimeField(auto_now_add=True, description='Datetime of creation of object')
    updated_at = fields.DatetimeField(auto_now=True, description='Datetime of last update of object')

    class Meta:
        abstract = True
        table_description = 'BaseModel with id field and timestamps'
