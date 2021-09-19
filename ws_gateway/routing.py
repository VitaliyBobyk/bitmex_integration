from django.urls import re_path
from . import consumers

urlpatterns = [
    re_path(r'', consumers.BitmexConsumer.as_asgi(), name='index'),
]