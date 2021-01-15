import asynctest
from typing import Awaitable
from tortoise.contrib.test import finalizer, initializer
from tortoise.fields import ReverseRelation
from app.models import *
from app.models.BaseModel import BaseModel


class PlaceModelTestCase(asynctest.TestCase):
    def setUp(self) -> None:
        initializer(['app.models'])

    def tearDown(self) -> None:
        finalizer()

    async def test_can_instance_model(self):
        rest = PlaceModel()
        self.assertIsInstance(rest, BaseModel)

    async def test_model_table_name(self):
        rest = PlaceModel()
        self.assertEqual(rest.Meta.table, 'place')

    async def test_model_has_req_fields(self):
        place = PlaceModel()
        self.assertIsNone(place.id)
        self.assertIsNone(place.created_at)
        self.assertIsNone(place.updated_at)
        self.assertIsNone(place.address)
        self.assertIsNone(place.longitude)
        self.assertIsNone(place.latitude)
        self.assertIsInstance(place.gallery, ReverseRelation)
        self.assertEqual(place.work_time_start, '')
        self.assertEqual(place.work_time_stop, '')
        self.assertEqual(place.preorder, False)
        self.assertIsInstance(place.tables, ReverseRelation)
        self.assertIsInstance(place.restaurant, Awaitable)
        self.assertEqual(place.rating, 25)
