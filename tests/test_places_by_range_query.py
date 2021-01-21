from tortoise.contrib.test import initializer, finalizer, IsolatedTestCase
from graphene import Schema
from graphene.test import Client
from app.models import FileModel, PlaceModel
from app.schema import DefaultSchema
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.models.RestaurantModel import RestaurantModel


class PlacesByRangeQueryTestCase(IsolatedTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        initializer(['app.models'], db_url='postgres://postgres:1@localhost:5432/test_{}')

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()

    async def setUp(self) -> None:
        self.schema: Schema = DefaultSchema.get_schema()
        self.client: Client = Client(schema=self.schema, executor=AsyncioExecutor(), return_promise=True)

    async def test_can_get_places_by_range(self):
        image = await FileModel.create(path='ttt')
        rest = RestaurantModel(name='test2', image=image)
        my_long = 59.9434583
        my_lat = 30.2815553
        my_dist = 0.5
        my_far_dist = 10
        await rest.save()
        await PlaceModel.create(address='dd', longitude=59.9445219, latitude=30.2824162, work_time='', restaurant=rest)
        await PlaceModel.create(address='dd2', longitude=59.939869, latitude=30.2712383, work_time='', restaurant=rest)
        result = await self.client.execute(f"""
            query {{
                placesByRange(latitude: {my_lat}, longitude: {my_long}, distance: {my_dist}) {{
                    id
                    address
                }}
            }}""")
        self.assertListEqual(result['data']['placesByRange'], [{'id': '1', 'address': 'dd'}])
        result2 = await self.client.execute(f"""
            query {{
                placesByRange(latitude: {my_lat}, longitude: {my_long}, distance: {my_far_dist}) {{
                    id
                }}
            }}""")
        self.assertListEqual(result2['data']['placesByRange'], [{'id': '1'}, {'id': '2'}])
