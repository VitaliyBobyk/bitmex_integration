import time
import ctypes
import threading

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from bitmex_websocket import BitMEXWebsocket


class WebSocket:

    def __init__(self, api_key, api_secret, symbol, group_name, account_name):
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbol = symbol
        self.group_name = group_name
        self.account_name = account_name
        self.ws = BitMEXWebsocket(
            endpoint="https://testnet.bitmex.com/api/v1",
            symbol=self.symbol,
            api_key=self.api_key,
            api_secret=self.api_secret
        )

    def close_connection(self):
        if self.ws.ws.sock.connected:
            self.ws.exit()

    def get_data(self):
        channel_layer = get_channel_layer()
        while (self.ws.ws.sock.connected):
            data = self.ws.get_instrument()
            response = {
                'timestamp': data['timestamp'],
                'account': self.account_name,
                'symbol': self.symbol,
                'price': data['markPrice']
            }
            async_to_sync(channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'auto_update',
                    'data': response
                }
            )
            time.sleep(1)


def thread_is_running(name):
    for t in threading.enumerate():
        if t.name == name:
            return True
    return False


def stop_thread(name):
    for t in threading.enumerate():
        if t.name == name:
            exc = ctypes.py_object(SystemExit)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(t.ident), exc)
            if res == 0:
                raise ValueError("nonexistent thread id")
            elif res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(t.ident, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
