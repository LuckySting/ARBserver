from typing import List

from graphene import ResolveInfo
from app.models import RestaurantModel, FileModel, DishModel
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
    async def resolve_dish_image(cls, parent: RestaurantModel, info: ResolveInfo) -> FileModel:
        image = await parent.image.first()
        return image
