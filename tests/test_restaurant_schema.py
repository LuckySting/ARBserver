import unittest

from graphene import Schema
from graphene.test import Client
from app.schema import DefaultSchema


class RestaurantSchemaTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.schema: Schema = DefaultSchema.get_schema()
        self.client: Client = Client(schema=self.schema)

    def test_can_execute_restaurants_query(self):
        result = self.client.execute("""
            query {
                restaurants {
                    id
                }
            }""")
        self.assertIsNotNone(result['data'])
        self.assertListEqual(result['data'], [])
