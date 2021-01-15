from datetime import datetime
from typing import List

from graphene import ResolveInfo
from app.models import RestaurantModel, FileModel, DishModel, PlaceModel, TableModel
from .OrderByPaginationResolver import OrderByPaginationResolver


class RestaurantResolver(OrderByPaginationResolver):
    @classmethod
    async def resolve_restaurants(cls, info: ResolveInfo, order_by: 'OrderByType',
                                  pagination: 'PaginationType') -> List[RestaurantModel]:
        restaurants = RestaurantModel.all()
        return await cls.order_by_pagination(restaurants, order_by, pagination)

    @classmethod
    async def resolve_restaurant(cls, info: ResolveInfo, id: str) -> RestaurantModel:
        restaurant = await RestaurantModel.get_or_none(id=int(id))
        return restaurant

    @classmethod
    async def resolve_restaurant_image(cls, parent: RestaurantModel, info: ResolveInfo) -> FileModel:
        image = await parent.image.first()
        return image

    @classmethod
    async def resolve_dish_restaurant(cls, parent: DishModel, info: ResolveInfo) -> RestaurantModel:
        restaurant = await parent.restaurant.first()
        return restaurant

    @classmethod
    async def resolve_restaurant_menu(cls, parent: RestaurantModel, info: ResolveInfo, order_by: 'OrderByType',
                                      pagination: 'PaginationType') -> List[DishModel]:
        menu = await cls.order_by_pagination(parent.menu.all(), order_by, pagination)
        return menu

    @classmethod
    async def resolve_dish_image(cls, parent: DishModel, info: ResolveInfo) -> FileModel:
        image = await parent.image.first()
        return image

    @classmethod
    async def resolve_place_restaurant(cls, parent: PlaceModel, info: ResolveInfo) -> RestaurantModel:
        restaurant = await parent.restaurant.first()
        return restaurant

    @classmethod
    async def resolve_restaurant_places(cls, parent: RestaurantModel, info: ResolveInfo, order_by: 'OrderByType',
                                        pagination: 'PaginationType') -> List[PlaceModel]:
        places = await cls.order_by_pagination(parent.places.all(), order_by, pagination)
        return places

    @classmethod
    async def resolve_table_place(cls, parent: TableModel, info: ResolveInfo) -> PlaceModel:
        place = await parent.place.first()
        return place

    @classmethod
    async def resolve_place_tables(cls, parent: PlaceModel, info: ResolveInfo, order_by: 'OrderByType',
                                   pagination: 'PaginationType') -> List[TableModel]:
        tables = await cls.order_by_pagination(parent.tables.all(), order_by, pagination)
        return tables

    @classmethod
    async def resolve_place_gallery(cls, parent: PlaceModel, info: ResolveInfo, order_by: 'OrderByType',
                                    pagination: 'PaginationType') -> List[FileModel]:
        gallery = await cls.order_by_pagination(parent.gallery.all(), order_by, pagination)
        return gallery

    @classmethod
    async def resolve_restaurant_last_place_created_at(cls, parent: RestaurantModel, info: ResolveInfo) -> datetime:
        last_created_place: PlaceModel = await parent.places.order_by('created_at').first()
        return last_created_place.created_at
