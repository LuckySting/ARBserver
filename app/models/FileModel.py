from app.models.BaseModel import BaseModel
from tortoise import fields


class FileModel(BaseModel):
    class Meta:
        table = 'file'

    path = fields.CharField(max_length=1000, description='Path to file')
