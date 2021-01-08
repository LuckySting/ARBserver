import asynctest
from typing import Awaitable
from tortoise.contrib.test import finalizer, initializer
from tortoise.fields import ReverseRelation

from app.models import RestaurantModel
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
