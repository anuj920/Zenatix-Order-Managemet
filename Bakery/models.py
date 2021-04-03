from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length = 250)
    price = models.DecimalField(decimal_places=2, default = 0.00, blank=True, null =True, max_digits = 10)

    def __str__(self):
        return self.name


class Bakery(models.Model):
    name = models.CharField(max_length = 250)
    quantity = models.IntegerField(default=0)
    cost_price = models.DecimalField(decimal_places=2, default = 0.00, blank=True, null =True, max_digits = 10)
    sell_price = models.DecimalField(decimal_places=2, default = 0.00, blank=True, null =True, max_digits = 10)
    
    def __str__(self):
        return self.name

class BakeryIngredientCombination(models.Model):
    bakery = models.ForeignKey(Bakery, on_delete=models.CASCADE, related_name='bakery_ingredient')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='bakery_item_ingredient')
    ingredient_quantity = models.IntegerField(default=0)