from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name ='customer-register'),
    path('login/', views.Login.as_view(), name ='customer-login'),
    path('logout/', views.LogoutView.as_view(), name ='customer-logout'),
    path('order/', views.ProductOrder.as_view(), name ='customer-order'),
    path('product-list/', views.GetProductList.as_view(), name ='customer-product-list'),
]