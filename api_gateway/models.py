from django.db import models


SIDE_CHOICE = (
    ('buy', 'Buy'),
    ('sell', 'Sell')
)


class Account(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    api_key = models.TextField()
    api_secret = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, unique=True)
    symbol = models.CharField(max_length=255)
    volume = models.FloatField()
    timestamp = models.DateTimeField()
    side = models.CharField(max_length=255, choices=SIDE_CHOICE)
    price = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order: {self.order_id}, created by: {self.account.name}'
