from graphene import ObjectType, List, ResolveInfo, ID, Field, Float
import typing
from app.models import RestaurantModel, PlaceModel
from app.schema.types import RestaurantType, OrderByType, PaginationType, PlaceType
from app.resolvers.RestaurantResolver import RestaurantResolver


class DefaultQuery(ObjectType):
    restaurants = Field(List(RestaurantType), order_by=OrderByType(), pagination=PaginationType())
    restaurant = Field(RestaurantType, id=ID(required=True))
    placesByRange = Field(List(PlaceType), latitude=Float(required=True), longitude=Float(required=True),
                          distance=Float(required=True))

    async def resolve_restaurants(self, info: ResolveInfo, order_by: OrderByType = None,
                                  pagination: PaginationType = None) -> typing.List[RestaurantModel]:
        restaurants = await RestaurantResolver.resolve_restaurants(info, order_by, pagination)
        return restaurants

    async def resolve_restaurant(self, info: ResolveInfo, id: str) -> RestaurantModel:
        restaurant = await RestaurantResolver.resolve_restaurant(info, id)
        return restaurant

    async def resolve_placesByRange(self, info: ResolveInfo, latitude: float,
                                    longitude: float, distance: float) -> typing.List[PlaceModel]:
        places = await RestaurantResolver.resolve_places_by_range(info, latitude, longitude, distance)
        return places
