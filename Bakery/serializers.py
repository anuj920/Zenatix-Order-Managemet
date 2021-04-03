from rest_framework import serializers
from .models import Ingredient, Bakery, BakeryIngredientCombination



class IngredientModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'



class BakeryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bakery
        fields = '__all__'