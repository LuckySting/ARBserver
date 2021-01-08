import asynctest
from typing import Awaitable
from tortoise.contrib.test import finalizer, initializer
from app.models import TableModel
from app.models.BaseModel import BaseModel


class TableModelTestCase(asynctest.TestCase):
    def setUp(self) -> None:
        initializer(['app.models'])

    def tearDown(self) -> None:
        finalizer()

    async def test_can_instance_model(self):
        table = TableModel()
        self.assertIsInstance(table, BaseModel)

    async def test_model_table_name(self):
        table = TableModel()
        self.assertEqual(table.Meta.table, 'table')

    async def test_model_has_req_fields(self):
        table = TableModel()
        self.assertIsNone(table.id)
        self.assertIsNone(table.created_at)
        self.assertIsNone(table.updated_at)
        self.assertIsInstance(table.place, Awaitable)
        self.assertIsNone(table.name)
        self.assertTrue(table.available)
        self.assertIsNone(table.capacity)
        self.assertFalse(table.smoking)
        self.assertEqual(table.description, '')
        self.assertIsInstance(table.image, Awaitable)
