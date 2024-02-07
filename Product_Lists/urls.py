from django.urls import path
from .views import product_lists

urlpatterns = [
    path('', product_lists, name='product_list'),
]
