from typing import Awaitable

import asynctest
from tortoise.contrib.test import finalizer, initializer
from tortoise.fields import ReverseRelation

from app.models import RestaurantModel, FileModel
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
        self.assertIsInstance(rest.menu, ReverseRelation)
        self.assertIsInstance(rest.places, ReverseRelation)
        self.assertIsInstance(rest.image, Awaitable)

    async def test_can_create_restaurant(self):
        image = FileModel(path='t')
        await image.save()
        rest = RestaurantModel(name='Test', image=image)
        await rest.save()
        self.assertEqual(rest.id, 1)
        self.assertIsNotNone(rest.created_at)
        self.assertIsNotNone(rest.updated_at)
        self.assertEqual(rest.description, '')
        self.assertEqual(rest.confirmed, False)
        self.assertEqual(rest.name, 'Test')
        self.assertEqual(rest.image, image)
        self.assertIsInstance(rest.menu, ReverseRelation)
        self.assertIsInstance(rest.places, ReverseRelation)

    async def test_can_get_restaurant_list(self):
        image = FileModel(path='t1')
        image2 = FileModel(path='t2')
        await image.save()
        await image2.save()
        rest = RestaurantModel(name='t1', image=image)
        rest2 = RestaurantModel(name='t2', image=image2)
        await rest.save()
        await rest2.save()
        rests = await RestaurantModel.all()
        rests_objs = [(r.id, r.name, await r.image.first()) for r in rests]
        self.assertListEqual(rests_objs, [(1, 't1', image), (2, 't2', image2)])

    async def test_can_get_restaurant_by_id(self):
        image = FileModel(path='t1')
        await image.save()
        rest = RestaurantModel(name='t1', image=image)
        await rest.save()
        rest_obj = await RestaurantModel.get(id=1)
        self.assertEqual(rest, rest_obj)
