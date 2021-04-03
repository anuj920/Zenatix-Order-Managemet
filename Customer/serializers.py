from rest_framework import serializers
from .models import Order, OrderItem
from Bakery.models import Bakery


class OrderModelSerializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = '__all__'

    
    def get_order_item(self, obj):
        order_item = obj.order_item.values('bakery__name', 'quantity')
        return order_item