import asyncio
from tortoise.contrib.test import initializer, finalizer, IsolatedTestCase
from graphene import Schema
from graphene.test import Client
from app.models import FileModel
from app.schema import DefaultSchema
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.models.RestaurantModel import RestaurantModel


class RestaurantsQueryTestCase(IsolatedTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        initializer(['app.models'])

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()

    async def setUp(self) -> None:
        self.schema: Schema = DefaultSchema.get_schema()
        self.client: Client = Client(schema=self.schema, executor=AsyncioExecutor(), return_promise=True)

    async def test_can_get_restaurants(self):
        image = await FileModel.create(path='t')
        rest = RestaurantModel(name='test', image=image)
        await rest.save()
        result = await self.client.execute("""
            query {
                restaurants {
                    id
                }
            }""")
        self.assertIsNotNone(result['data'])
        self.assertIsNotNone(result['data']['restaurants'])
        self.assertListEqual(result['data']['restaurants'], [{'id': str(rest.id)}])

    async def test_can_order_restaurants(self):
        image = await FileModel.create(path='t')
        await RestaurantModel.create(name='test', image=image)
        await RestaurantModel.create(name='test2', image=image)
        result = await self.client.execute("""
            query {
                restaurants(orderBy: {field: "id"}) {
                    id
                }
            }""")
        result2 = await self.client.execute("""
            query {
                restaurants(orderBy: {field: "id", desk: true}) {
                    id
                }
            }""")
        self.assertListEqual(result['data']['restaurants'], [{'id': '1'}, {'id': '2'}])
        self.assertListEqual(result2['data']['restaurants'], [{'id': '2'}, {'id': '1'}])

    async def test_can_order_restaurants_using_camelcase_and_snake_case(self):
        image = await FileModel.create(path='t')
        await RestaurantModel.create(name='test', image=image)
        await asyncio.sleep(0.2)
        await RestaurantModel.create(name='test2', image=image)
        result = await self.client.execute("""
            query {
                restaurants(orderBy: {field: "createdAt"}) {
                    id
                }
            }""")
        result2 = await self.client.execute("""
            query {
                restaurants(orderBy: {field: "createdAt", desk: true}) {
                    id
                }
            }""")
        result3 = await self.client.execute("""
                query {
                    restaurants(orderBy: {field: "created_at", desk: true}) {
                        id
                    }
                }""")
        self.assertListEqual(result['data']['restaurants'], [{'id': '1'}, {'id': '2'}])
        self.assertListEqual(result2['data']['restaurants'], [{'id': '2'}, {'id': '1'}])
        self.assertListEqual(result2['data']['restaurants'], result3['data']['restaurants'])

    async def test_can_paginate_restaurants(self):
        image = await FileModel.create(path='t')
        await RestaurantModel.create(name='test', image=image)
        await RestaurantModel.create(name='test2', image=image)
        result = await self.client.execute("""
            query {
                restaurants(pagination: {limit: 1, page: 1}) {
                    id
                }
            }""")
        result2 = await self.client.execute("""
            query {
                restaurants(pagination: {limit: 1, page: 2}) {
                    id
                }
            }""")
        self.assertListEqual(result['data']['restaurants'], [{'id': '1'}])
        self.assertListEqual(result2['data']['restaurants'], [{'id': '2'}])
