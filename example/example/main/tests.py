

from django.test import TestCase
from django.core.urlresolvers import reverse

from ..utils.testing import TestRpcClient


class MainTestCase(TestCase):

    def setUp(self):
        self.client = TestRpcClient()

    def test_base(self):
        api_url = reverse('main:rpc:jsapi')
        router_url = reverse('main:rpc:router')

        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.call(router_url, 'MainApi', 'hello', ['username'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['result'], {'msg': 'Hello, username'})
