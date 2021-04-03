from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ingredient', views.IngredientView, basename='bakery-ingredient')


urlpatterns = [
    path('login/', views.Login.as_view(), name ='bakery-login'),
    path('bakery-create-update/', views.BakeryView.as_view(), name ='bakery-create-update'),
    path('hot-selling-product/', views.GetHotSellingProduct.as_view(), name ='hot-selling-product'),
] + router.urls