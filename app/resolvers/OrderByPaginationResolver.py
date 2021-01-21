import re

from tortoise.queryset import QuerySet
from typing import List, Any


def to_camel_case(string: str) -> str:
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()


class OrderByPaginationResolver:
    @classmethod
    async def order_by_pagination(cls, queryset: QuerySet, order_by: 'OrderByType', pagination: 'PaginationType') -> \
    List[Any]:
        if order_by is not None:
            order_by.field = to_camel_case(order_by.field)
            if order_by.desk:
                queryset = queryset.order_by(f'-{order_by.field}')
            else:
                queryset = queryset.order_by(order_by.field)
        if pagination is not None:
            queryset = queryset.offset(pagination.limit * (pagination.page - 1)).limit(pagination.limit)
        return await queryset
