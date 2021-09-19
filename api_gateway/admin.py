from django.contrib import admin

from api_gateway.models import Account, Order

admin.site.register(Order)
admin.site.register(Account)

