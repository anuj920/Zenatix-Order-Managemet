from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from Bakery.models import Bakery
from .models import Order, OrderItem
from .utils import generateOrderId
from .serializers import OrderModelSerializer



class Login(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user_exists = User.objects.filter(username=username)
            if not user_exists.exists():
                return Response({"message": "User with this details not exists.", "flag": False},
                                status=status.HTTP_400_BAD_REQUEST)
            user_obj = authenticate(username=user_exists[0].username, password=password)
            if user_obj:
                if user_obj.is_active:
                    user_token, created = Token.objects.get_or_create(user=user_obj)
                    return Response({"message":"Logged in","token":user_token.key,"username":user_obj.username, "flag": True},status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Please activate your account to login.", "flag": False},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message": 'Password Incorrect', "flag": False}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {'message': 'Please enter a valid username and password.', "details": str(e), "flag": False},
                status=status.HTTP_401_UNAUTHORIZED)


class Register(APIView):

    def post(self, request):
        username = request.data.get("username")
        password1 = request.data.get("password")
        password2 = request.data.get("re-password")
        if password1 == password2:
            user_exists = User.objects.filter(username=username)
            if user_exists.exists():
                return Response({"message": "User with this details exists.", "flag": False},status=status.HTTP_400_BAD_REQUEST)
            user_obj = User.objects.create_user(username=username, email=username, password=password1)
            return Response({"message": 'User Created', "flag": True}, status=201)
        else:
            return Response({'message': 'Both Password not match.', "flag": False},status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(DestroyAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        """
        """
        return self.request.auth



class GetProductList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        pro_obj = Bakery.objects.filter(quantity__gt=0).values()
        return Response({"product_list":pro_obj}, status=200)

    

class ProductOrder(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


    def post(self, request):
        data = request.data
        product_list = data.get('product')
        if product_list:
            order_id = generateOrderId()
            order_obj = Order.objects.create(user = request.user, order_id = order_id)
            product_list_obj = []
            quantity_list_obj = []
            amount = 0
            try:
                for product in product_list:
                    bakery_obj = Bakery.objects.get(id = int(product.get('product_id')))
                    if not bakery_obj.quantity < product.get('quantity'):
                        product_list_obj.append(OrderItem(order = order_obj, bakery = bakery_obj, quantity = product.get('quantity')))
                        amount+=bakery_obj.sell_price
                        bakery_obj.quantity -= product.get('quantity')
                        quantity_list_obj.append(bakery_obj)
                    else:
                        raise ValidationError("Bakery '"+ bakery_obj.name +"' Quantity Less than Required")
                        break
                order_obj.amount = amount
                order_obj.save()

                OrderItem.objects.bulk_create(product_list_obj)
                Bakery.objects.bulk_update(quantity_list_obj, ['quantity'])
                return Response({"order_id":order_obj.id, "order_number":order_id, "amount":amount, "message":"Order Successfully Created"}, status=201)
            except Exception as e:
                print(str(e))
                order_obj.delete()
                return Response({"message":"There is something wrong", "error":str(e)}, status=400)

    
    def get(self, request):
        order_obj = Order.objects.filter(user = request.user).prefetch_related('order_item')
        ser  = OrderModelSerializer(order_obj, many = True)
        return Response(ser.data, status=200)