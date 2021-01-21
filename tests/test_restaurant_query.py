from datetime import datetime

from tortoise.contrib.test import initializer, finalizer, IsolatedTestCase
from graphene import Schema
from graphene.test import Client
from app.models import FileModel, DishModel, PlaceModel, TableModel, PlaceGalleryModel
from app.schema import DefaultSchema
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.models.RestaurantModel import RestaurantModel


class RestaurantQueryTestCase(IsolatedTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        initializer(['app.models'])

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()

    async def setUp(self) -> None:
        self.schema: Schema = DefaultSchema.get_schema()
        self.client: Client = Client(schema=self.schema, executor=AsyncioExecutor(), return_promise=True)

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

    async def test_can_get_restaurant_menu(self):
        image = await FileModel.create(path='ttt')
        rest = RestaurantModel(name='test2', image=image)
        await rest.save()
        dish1 = DishModel(name='test', image=image, restaurant=rest, price=123)
        await dish1.save()
        result = await self.client.execute(f"""
            query {{
                restaurant(id: "{rest.id}") {{
                    id
                    name
                    menu {{
                        id
                        name
                        image {{
                            path
                        }}
                        price
                        restaurant {{
                            id
                            name
                        }}
                    }}
                }}
            }}""")
        self.assertIsNotNone(result['data'])
        self.assertIsNotNone(result['data']['restaurant'])
        menu = result['data']['restaurant']['menu']
        self.assertEqual(len(menu), 1)
        dish = menu[0]
        self.assertEqual(dish['id'], '1')
        self.assertEqual(dish['name'], 'test')
        self.assertEqual(dish['image']['path'], 'ttt')
        self.assertEqual(dish['price'], 123)
        self.assertEqual(result['data']['restaurant']['menu'][0]['restaurant']['id'],
                         result['data']['restaurant']['id'])
        self.assertEqual(result['data']['restaurant']['menu'][0]['restaurant']['name'],
                         result['data']['restaurant']['name'])

    async def test_can_get_restaurant_places(self):
        image = await FileModel.create(path='ttt')
        rest = RestaurantModel(name='test2', image=image)
        await rest.save()
        await PlaceModel.create(address='dd', longitude=0, latitude=0, work_time='', restaurant=rest)
        await PlaceModel.create(address='dd2', longitude=0, latitude=0, work_time='', restaurant=rest)
        result = await self.client.execute(f"""
            query {{
                restaurant(id: "{rest.id}") {{
                    id
                    places {{
                        id
                        restaurant {{
                            id
                        }}
                    }}
                }}
            }}""")
        self.assertIsNotNone(result['data'])
        self.assertIsNotNone(result['data']['restaurant'])
        places = result['data']['restaurant']['places']
        self.assertEqual(len(places), 2)
        self.assertEqual(places[0]['restaurant']['id'], result['data']['restaurant']['id'])

    async def test_can_get_restaurant_place_tables(self):
        image = await FileModel.create(path='ttt')
        rest = RestaurantModel(name='test2', image=image)
        await rest.save()
        place = await PlaceModel.create(address='dd', longitude=0, latitude=0, work_time='', restaurant=rest)
        await TableModel.create(name='sdf', capacity=4, image=image, place=place)
        result = await self.client.execute(f"""
            query {{
                restaurant(id: "{rest.id}") {{
                    id
                    places {{
                        id
                        tables {{
                            id
                            name
                            capacity
                            place {{
                                id
                            }}
                        }}
                    }}
                }}
            }}""")
        self.assertIsNotNone(result['data'])
        self.assertIsNotNone(result['data']['restaurant'])
        places = result['data']['restaurant']['places']
        tables = places[0]['tables']
        self.assertEqual(tables[0], {'id': '1', 'name': 'sdf', 'capacity': 4, 'place': {'id': '1'}})

    async def test_can_get_restaurant_place_gallery(self):
        image = await FileModel.create(path='ttt')
        rest = RestaurantModel(name='test2', image=image)
        await rest.save()
        place = await PlaceModel.create(address='dd', longitude=0, latitude=0, work_time='', restaurant=rest)
        img1 = await FileModel.create(path='1')
        img2 = await FileModel.create(path='2')
        await PlaceGalleryModel.create(file=img1, place=place)
        await PlaceGalleryModel.create(file=img2, place=place)
        result = await self.client.execute(f"""
            query {{
                restaurant(id: "{rest.id}") {{
                    id
                    places {{
                        gallery {{
                            path
                        }}
                    }}
                }}
            }}""")
        place = result['data']['restaurant']['places'][0]
        gallery = place['gallery']
        self.assertListEqual(gallery, [{'path': '1'}, {'path': '2'}])

    async def test_can_get_restaurant_last_place_created_at(self):
        image = await FileModel.create(path='ttt')
        rest = RestaurantModel(name='test2', image=image)
        await rest.save()
        place = await PlaceModel.create(address='dd', longitude=0, latitude=0, work_time='', restaurant=rest)
        result = await self.client.execute(f"""
            query {{
                restaurant(id: "{rest.id}") {{
                    lastPlaceCreatedAt
                }}
            }}""")
        self.assertEqual(datetime.fromisoformat(result['data']['restaurant']['lastPlaceCreatedAt']), place.created_at)