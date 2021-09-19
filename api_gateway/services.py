import sys
import json

import bitmex


class BitmexClient:

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = bitmex.bitmex(test=True, api_key=self.api_key, api_secret=self.api_secret)

    def make_order(self, symbol, side, volume, price):
        return self.client.Order.Order_new(symbol=symbol, side=side.title(), orderQty=volume, price=price).result()

    def delete_order(self, order_id):
        if 'test' not in sys.argv:
            return self.client.Order.Order_cancel(orderID=order_id).result()
