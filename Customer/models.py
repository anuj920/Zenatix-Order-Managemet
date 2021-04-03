from django.db import models
from django.contrib.auth.models import User
from Bakery.models import Bakery

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    order_id = models.CharField(max_length = 50)
    amount = models.DecimalField(decimal_places=2, default = 0.00, blank=True, null =True, max_digits = 10)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    bakery = models.ForeignKey(Bakery, on_delete=models.CASCADE, related_name='bakery_order')
    quantity = models.IntegerField(default=0)

