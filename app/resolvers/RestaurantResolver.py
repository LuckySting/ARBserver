from typing import List

from graphene import ResolveInfo
from app.models import RestaurantModel
from app.schema.types import OrderByType, PaginationType


class RestaurantResolver:
    @classmethod
    async def resolve_restaurants(cls, info: ResolveInfo, order_by: OrderByType,
                                  pagination: PaginationType) -> List[RestaurantModel]:
        restaurants = RestaurantModel.all()
        if order_by is not None:
            if order_by.desk:
                restaurants = restaurants.order_by(f'-{order_by.field}')
            else:
                restaurants = restaurants.order_by(order_by.field)
        if pagination is not None:
            restaurants = restaurants.offset(pagination.limit * (pagination.page - 1)).limit(pagination.limit)
        return await restaurants

    @classmethod
    async def resolve_restaurant(cls, info: ResolveInfo, id: str) -> RestaurantModel:
        restaurant = await RestaurantModel.get_or_none(id=int(id))
        return restaurant
