from app.models.BaseModel import BaseModel
from tortoise import fields


class RestaurantModel(BaseModel):
    class Meta:
        table = 'restaurant'
        table_description = 'Represents restaurant'

    name = fields.CharField(max_length=50, description='Name of the restaurant')
    description = fields.TextField(default='', description='Description of the restaurant')
    confirmed = fields.BooleanField(default=False, description='Is restaurant is validated by moderator')
    image = fields.CharField(max_length=200, description='URL for getting restaurant image for main page')
