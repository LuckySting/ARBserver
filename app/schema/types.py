from graphene import ObjectType, ID, String, Boolean, Int, InputObjectType, Field, ResolveInfo

from app.models import FileModel, RestaurantModel
from app.resolvers.RestaurantResolver import RestaurantResolver


class OrderByType(InputObjectType):
    field = String(required=True)
    desk = Boolean(default_value=False)


class PaginationType(InputObjectType):
    limit = Int(default_value=10)
    page = Int(default_value=1)


class FileType(ObjectType):
    path = String(required=True)


class RestaurantType(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    image = Field(FileType)
    description = String(required=True)
    confirmed = Boolean(required=True)

    async def resolve_image(parent: RestaurantModel, info: ResolveInfo) -> FileModel:
        image = await RestaurantResolver.resolve_restaurant_image(parent, info)
        return image
