import typing
from graphene import ObjectType, ID, String, Boolean, Int, InputObjectType, Field, ResolveInfo, DateTime, Float, List

from app.models import FileModel, RestaurantModel, DishModel, PlaceModel, TableModel
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
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)
    menu = List('app.schema.types.DishType')
    places = List('app.schema.types.PlaceType')

    async def resolve_image(parent: RestaurantModel, info: ResolveInfo) -> FileModel:
        image = await RestaurantResolver.resolve_restaurant_image(parent, info)
        return image

    async def resolve_menu(parent: RestaurantModel, info: ResolveInfo, order_by: OrderByType = None,
                           pagination: PaginationType = None) -> typing.List[DishModel]:
        menu = await RestaurantResolver.resolve_restaurant_menu(parent, info, order_by, pagination)
        return menu

    async def resolve_places(parent: RestaurantModel, info: ResolveInfo, order_by: OrderByType = None,
                             pagination: PaginationType = None) -> typing.List[PlaceModel]:
        menu = await RestaurantResolver.resolve_restaurant_places(parent, info, order_by, pagination)
        return menu


class DishType(ObjectType):
    id = ID(required=True)
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)
    name = String(required=True)
    image = Field(FileType)
    price = Float(required=True)
    sale = Boolean(required=True)
    sale_price = Float(required=True)
    restaurant = Field(RestaurantType, required=True)

    async def resolve_restaurant(parent: DishModel, info: ResolveInfo) -> RestaurantModel:
        restaurant = await RestaurantResolver.resolve_dish_restaurant(parent, info)
        return restaurant

    async def resolve_image(parent: DishModel, info: ResolveInfo) -> FileModel:
        image = await RestaurantResolver.resolve_dish_image(parent, info)
        return image


class PlaceType(ObjectType):
    id = ID(required=True)
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)
    address = String(required=True)
    longitude = Float(required=True)
    latitude = Float(required=True)
    # gallery: List(FileType) TODO
    work_time = String(required=True)
    preorder = Boolean(required=True)
    restaurant = Field(RestaurantType, required=True)
    tables = List('app.schema.types.TableType')

    async def resolve_restaurant(parent: PlaceModel, info: ResolveInfo) -> RestaurantModel:
        restaurant = await RestaurantResolver.resolve_place_restaurant(parent, info)
        return restaurant

    async def resolve_tables(parent: PlaceModel, info: ResolveInfo, order_by: OrderByType = None,
                             pagination: PaginationType = None) -> typing.List[TableModel]:
        tables = await RestaurantResolver.resolve_place_tables(parent, info, order_by, pagination)
        return tables


class TableType(ObjectType):
    id = ID(required=True)
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)
    available = Boolean(required=True)
    capacity = Int(required=True)
    smoking = Boolean(required=True)
    name = String(required=True)
    description = String(required=True)
    image = Field(FileType)
    place = Field(PlaceType, required=True)

    async def resolve_place(parent: TableModel, info: ResolveInfo) -> PlaceModel:
        place = await RestaurantResolver.resolve_table_place(parent, info)
        return place
