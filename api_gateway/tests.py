import uuid
import datetime

from django.urls import reverse

from rest_framework.test import APIRequestFactory, APITestCase

from api_gateway.models import Account, Order
from api_gateway.views import OrdersView, AccountCreateVIew, OrderDetailView


class TestSetup(APITestCase):
    def setUp(self):
        self.order_id = None
        self.account_url = reverse('api:account')
        self.orders_url = reverse('api:orders')
        self.factory = APIRequestFactory()
        self.account = Account.objects.create(
            name='test',
            api_key='CvX2RR2VKfQrnZui5vbyMDqk',
            api_secret='UTZoA6PC7jZBlwWv-AiTQFIdR1TRyh-pH_08g6pKuJpECM20'
        )
        self.order = Order.objects.create(
            order_id=str(uuid.uuid4()),
            symbol='XBTUSD',
            volume=1.0,
            side='buy',
            price=100000.0,
            timestamp=datetime.datetime.now(),
            account=self.account
        )
        self.headers = {'account': self.account.name}
        return super().setUp()

    def get_request(self, url, data=None, headers=None):
        request = self.factory.get(url, data=data, format='json')
        if headers:
            request.headers = headers
        return request

    def post_request(self, url, data=None, headers=None):
        request = self.factory.post(url, data=data, format='json')
        if headers:
            request.headers = headers
        return request

    def delete_request(self, url, data=None, headers=None):
        request = self.factory.delete(url, data=data, format='json')
        if headers:
            request.headers = headers
        return request


class TestViews(TestSetup):
    def test_account_create(self):
        json_body = {
            'name': 'unit_tester',
            'api_key': 'CvX2RR2VKfQrnZui5vbyMDqk',
            'api_secret': 'UTZoA6PC7jZBlwWv-AiTQFIdR1TRyh-pH_08g6pKuJpECM20'
        }

        # Test request with invalid json schema
        invalid_json_request = self.post_request(
            url=self.orders_url,
            data=json_body['name'],
            headers=self.headers
        )
        invalid_json_response = AccountCreateVIew.as_view()(invalid_json_request)
        self.assertEqual(invalid_json_response.status_code, 400)

        # Test request with valid data
        valid_request = self.post_request(
            url=self.orders_url,
            data=json_body,
            headers=self.headers
        )
        invalid_missing_headers_response = AccountCreateVIew.as_view()(valid_request)
        self.assertEqual(invalid_missing_headers_response.status_code, 201)

    def test_order_create(self):
        json_body = {
            "symbol": "XRPUSD",
            "volume": 1.0,
            "side": "buy",
            "price": 0.1
        }

        # Test request with invalid json schema
        invalid_json_request = self.post_request(
            url=self.orders_url,
            data=json_body['volume'],
            headers=self.headers
        )
        invalid_json_response = OrdersView.as_view()(invalid_json_request)
        self.assertEqual(invalid_json_response.status_code, 400)

        # Test request with missing account in headers
        invalid_missing_headers_request = self.post_request(
            url=self.orders_url,
            data=json_body,
        )
        invalid_missing_headers_response = OrdersView.as_view()(invalid_missing_headers_request)
        self.assertEqual(invalid_missing_headers_response.status_code, 400)

        # Test request with valid data
        valid_request = self.post_request(
            url=self.orders_url,
            data=json_body,
            headers=self.headers
        )
        invalid_missing_headers_response = OrdersView.as_view()(valid_request)
        self.assertEqual(invalid_missing_headers_response.status_code, 201)

    def test_get_orders(self):
        # Test request with missing account in headers
        invalid_missing_headers_request = self.get_request(
            self.orders_url,
        )
        invalid_missing_headers_response = OrdersView.as_view()(invalid_missing_headers_request)
        self.assertEqual(invalid_missing_headers_response.status_code, 400)

        # Test request with valid data
        valid_request = self.get_request(
            self.orders_url,
            headers=self.headers
        )
        valid_response = OrdersView.as_view()(valid_request)
        self.assertEqual(valid_response.status_code, 200)

    def test_get_order(self):
        url = reverse('api:order_detail', kwargs={'pk': str(self.order.order_id)})

        # Test request with missing account in headers
        invalid_missing_headers_request = self.get_request(
            url=url,
        )
        invalid_missing_headers_response = OrderDetailView.as_view()(
            invalid_missing_headers_request,
            str(self.order.order_id)
        )
        self.assertEqual(invalid_missing_headers_response.status_code, 400)

        # Test request with valid data
        valid_request = self.get_request(
            url=url,
            headers=self.headers
        )
        valid_response = OrderDetailView.as_view()(
            valid_request,
            str(self.order.order_id)
        )
        self.assertEqual(valid_response.status_code, 200)

    def test_delete_order(self):
        url = reverse('api:order_detail', kwargs={'pk': str(self.order.order_id)})

        # Test request with missing account in headers
        invalid_missing_headers_request = self.delete_request(
            url=url,
        )
        invalid_missing_headers_response = OrderDetailView.as_view()(
            invalid_missing_headers_request,
            str(self.order.order_id)
        )
        self.assertEqual(invalid_missing_headers_response.status_code, 400)

        # Test request with valid data
        valid_request = self.delete_request(
            url=url,
            headers=self.headers
        )
        valid_response = OrderDetailView.as_view()(
            valid_request,
            str(self.order.order_id)
        )
        self.assertEqual(valid_response.status_code, 200)
