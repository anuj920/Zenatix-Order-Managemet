from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# Create your views here.

from .serializers import IngredientModelSerializer, BakeryModelSerializer
from .models import Ingredient, Bakery, BakeryIngredientCombination
from .decorators import user_is_superuser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from Customer.models import OrderItem
from django.db.models import Sum


class IngredientView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    serializer_class = IngredientModelSerializer

    def get_queryset(self):
        return Ingredient.objects.all()


    @user_is_superuser
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @user_is_superuser
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        ingre_obj = Ingredient.objects.filter(name__iexact = data.get('name')).first()
        if not ingre_obj:
            serializer.save()
            return Response({"message":"Ingredient Created", "data":serializer.data}, status=201)
        ingre_obj.price = data.get('price')
        ingre_obj.save()
        return Response({"message":"Ingredient Price Updated"}, status=200)



class BakeryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    @user_is_superuser
    def post(self, request):
        data = request.data
        bakery_obj = Bakery.objects.filter(name__iexact = data.get('name')).first()
        if not bakery_obj:
            bakery_obj = Bakery.objects.create(name = data.get('name'))
            cost = 0
            ingre_obj_list = []
            for ingre in data.get('ingredient'):
                ingre_obj = Ingredient.objects.get(id = ingre.get('ingredient'))
                ingre_obj_list.append(BakeryIngredientCombination(bakery =bakery_obj, ingredient = ingre_obj, ingredient_quantity = int(ingre.get('quantity'))))
                cost += float(ingre_obj.price) * int(ingre.get('quantity'))
            BakeryIngredientCombination.objects.bulk_create(ingre_obj_list)
            bakery_obj.cost_price = cost
            bakery_obj.sell_price = cost * 1.20
            bakery_obj.quantity = 1
            bakery_obj.save()
            return Response({"message":"BakeryItem Created", "data": BakeryModelSerializer(bakery_obj).data}, status=201)
        return Response({"message":"Bakery Item with name Already Exists, please Update the Quantity", "BakeryItem_id":bakery_obj.id},status=200)

    

    @user_is_superuser
    def get(self, request):
        bakery_obj = Bakery.objects.all().prefetch_related('bakery_ingredient').values()
        # for bakery in bakery_obj
        return Response(bakery_obj, status=200)
    
    
    @user_is_superuser
    def put(self, request):
        data = request.data
        bakery_obj = Bakery.objects.filter(name__iexact = data.get('name')).first()
        if bakery_obj:
            bakery_obj.quantity+=data.get('quantity')
            bakery_obj.save()
            return Response({"message":"Quantity Updated", "data": BakeryModelSerializer(bakery_obj).data}, status=200)
        return Response({"error":"No BakeryItem With this name exist"}, status=400)




class Login(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user_exists = User.objects.filter(username=username)
            if not user_exists.exists():
                return Response({"message": "User with this details not exists.", "flag": False},
                                status=400)
            user_obj = authenticate(username=user_exists[0].username, password=password)
            if user_obj:
                if user_obj.is_active:
                    user_token, created = Token.objects.get_or_create(user=user_obj)
                    return Response({"message":"Logged in","token":user_token.key,"username":user_obj.username, "flag": True},status=200)
                else:
                    return Response({"message": "Please activate your account to login.", "flag": False},status=401)
            else:
                return Response({"message": 'Password Incorrect', "flag": False}, status=401)
        except Exception as e:
            return Response({'message': 'Please enter a valid username and password.', "details": str(e), "flag": False},status=401)



class GetHotSellingProduct(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)


    @user_is_superuser
    def get(self, request):
        # Sending Top 5 Product
        obj = OrderItem.objects.all().values('bakery').annotate(product_quantity = Sum('quantity')).values('product_quantity', 'bakery__name').order_by('-product_quantity')[:5]
        return Response({"top_5_product":obj}, status=200)