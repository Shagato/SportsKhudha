from django.urls import path
from Product_Lists.views import *

urlpatterns = [
    path('', product_lists, name='product_list'),
    path('cart/', cart ,name='cart'),
    path('checkout/', checkout ,name='checkout'),
]
