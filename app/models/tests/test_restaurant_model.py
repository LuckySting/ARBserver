import asyncio

import asynctest
from tortoise.contrib.test import finalizer, initializer
from tortoise.fields import ReverseRelation

from app.models import *
from app.models.BaseModel import BaseModel


class RestaurantModelTestCase(asynctest.TestCase):
    def setUp(self) -> None:
        initializer(['app.models'])

    def tearDown(self) -> None:
        finalizer()

    async def test_can_instance_model(self):
        rest = RestaurantModel()
        self.assertIsInstance(rest, BaseModel)

    async def test_model_table_name(self):
        rest = RestaurantModel()
        self.assertEqual(rest.Meta.table, 'restaurant')

    async def test_model_has_req_fields(self):
        rest = RestaurantModel()
        self.assertIsNone(rest.id)
        self.assertIsNone(rest.created_at)
        self.assertIsNone(rest.updated_at)
        self.assertIsNone(rest.name)
        self.assertEqual(rest.description, '')
        self.assertEqual(rest.confirmed, False)
        self.assertIsNone(rest.image)
        self.assertIsInstance(rest.menu, ReverseRelation)
        self.assertIsInstance(rest.places, ReverseRelation)

    async def test_can_create_restaurant(self):
        rest = RestaurantModel()
        rest.name = 'Test'
        rest.image = 'test_url'
        await rest.save()
        self.assertEqual(rest.id, 1)
        self.assertIsNotNone(rest.created_at)
        self.assertIsNotNone(rest.updated_at)
        self.assertEqual(rest.description, '')
        self.assertEqual(rest.confirmed, False)
        self.assertEqual(rest.name, 'Test')
        self.assertEqual(rest.image, 'test_url')
        self.assertIsInstance(rest.menu, ReverseRelation)
        self.assertIsInstance(rest.places, ReverseRelation)

    async def test_can_get_restaurant_list(self):
        rest = RestaurantModel(name='t1', image='t1')
        rest2 = RestaurantModel(name='t2', image='t2')
        await rest.save()
        await rest2.save()
        rests = await RestaurantModel.all()
        rests_objs = [(r.id, r.name, r.image) for r in rests]
        self.assertListEqual(rests_objs, [(1, 't1', 't1'), (2, 't2', 't2')])

    async def test_can_get_restaurant_by_id(self):
        rest = RestaurantModel(name='t1', image='t1')
        await rest.save()
        rest_obj = await RestaurantModel.get(id=1)
        self.assertEqual(rest, rest_obj)
