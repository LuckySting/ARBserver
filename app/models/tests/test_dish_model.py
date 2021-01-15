import asynctest
from typing import Awaitable
from tortoise.contrib.test import finalizer, initializer
from app.models import *
from app.models.BaseModel import BaseModel


class DishModelTestCase(asynctest.TestCase):
    def setUp(self) -> None:
        initializer(['app.models'])

    def tearDown(self) -> None:
        finalizer()

    async def test_can_instance_model(self):
        dish = DishModel()
        self.assertIsInstance(dish, BaseModel)

    async def test_model_table_name(self):
        dish = DishModel()
        self.assertEqual(dish.Meta.table, 'dish')

    async def test_model_has_req_fields(self):
        dish = DishModel()
        self.assertIsNone(dish.id)
        self.assertIsNone(dish.created_at)
        self.assertIsNone(dish.updated_at)
        self.assertIsNone(dish.name)
        self.assertIsInstance(dish.image, Awaitable)
        self.assertIsNone(dish.price)
        self.assertEqual(dish.sale_price, 0)
        self.assertFalse(dish.sale)
        self.assertEqual(dish.description, '')
