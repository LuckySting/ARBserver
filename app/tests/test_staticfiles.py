from starlette.testclient import TestClient
from asynctest import IsolatedAsyncioTestCase
from app.app import create_test_app


class StaticfilesTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        self.app = create_test_app()
        self.client = TestClient(app=self.app)

    def test_can_get_bob_rest(self):
        result = self.client.get('/static/rests/bob/rest.jpg')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('image' in result.headers.get('content-type'))
