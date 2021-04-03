from django.contrib import admin
from .models import Bakery, Ingredient, BakeryIngredientCombination

# Register your models here.
admin.site.register(Bakery)
admin.site.register(Ingredient)
admin.site.register(BakeryIngredientCombination)
