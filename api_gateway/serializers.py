import sys
import uuid
import datetime

from bravado.exception import HTTPBadRequest
from rest_framework import serializers


from api_gateway.models import Account, Order
from api_gateway.services import BitmexClient

from django.core.exceptions import ObjectDoesNotExist


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

        extra_kwargs = {
            'order_id': {
                'read_only': True
            },
            'account': {
                'read_only': True
            },
            'timestamp': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        try:
            account = Account.objects.get(name=self.context["request"].headers.get('account'))
        except ObjectDoesNotExist as error:
            raise serializers.ValidationError(error)

        if 'test' in sys.argv:
            attrs['order_id'] = str(uuid.uuid4())
            attrs['price'] = 100000.00
            attrs['timestamp'] = datetime.datetime.now()
        else:
            bitmex = BitmexClient(
                account.api_key,
                account.api_secret,
            )
            try:
                resp = bitmex.make_order(
                    attrs['symbol'],
                    attrs['side'],
                    attrs['volume'],
                    attrs['price']
                )
                attrs['order_id'] = resp[0]['orderID']
                attrs['timestamp'] = resp[0]['timestamp']
            except HTTPBadRequest as error:
                raise serializers.ValidationError(error.swagger_result['error']['message'])
        return attrs


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

        extra_kwargs = {
            'timestamp': {
                'read_only': True
            },
        }