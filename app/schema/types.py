from graphene import ObjectType, ID, String, Boolean, Int, InputObjectType


class OrderByType(InputObjectType):
    field = String(required=True)
    desk = Boolean(default_value=False)


class PaginationType(InputObjectType):
    limit = Int(default_value=10)
    page = Int(default_value=1)


class RestaurantType(ObjectType):
    id = ID(required=True)
