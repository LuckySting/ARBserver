import asynctest
from tortoise.contrib.test import initializer, finalizer
from graphene import Schema
from graphene.test import Client

from app.models import FileModel
from app.schema import DefaultSchema
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.models.RestaurantModel import RestaurantModel


class RestaurantSchemaTestCase(asynctest.TestCase):

    def setUp(self) -> None:
        initializer(['app.models'])
        self.schema: Schema = DefaultSchema.get_schema()
        self.client: Client = Client(schema=self.schema, executor=AsyncioExecutor(), return_promise=True)

    def tearDown(self) -> None:
        finalizer()

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

    async def test_can_get_restaurant(self):
        image = await FileModel.create(path='ttt')
        rest = RestaurantModel(name='test2', image=image)
        await rest.save()
        result = await self.client.execute(f"""
            query {{
                restaurant(id: "{rest.id}") {{
                    id
                    name
                    image {{
                        path
                    }}
                    description
                    confirmed
                    createdAt
                    updatedAt
                }}
            }}""")
        self.assertIsNotNone(result['data'])
        self.assertIsNotNone(result['data']['restaurant'])
        restaurant = result['data']['restaurant']
        self.assertEqual(restaurant['id'], str(rest.id))
        self.assertEqual(restaurant['name'], 'test2')
        self.assertEqual(restaurant['image']['path'], 'ttt')
        self.assertEqual(restaurant['description'], '')
        self.assertEqual(restaurant['confirmed'], False)
        self.assertIsNotNone(restaurant['createdAt'])
        self.assertIsNotNone(restaurant['updatedAt'])
