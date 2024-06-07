from django.urls import path
from Product_Lists.views import *

urlpatterns = [
    path('', product_lists, name='product_list'),
    path('cart/', cart ,name='cart'),
    path('checkout/', checkout ,name='checkout'),
    path('update_item/', update_item ,name='update_item'),
    path('process_order/', processOrder ,name='process_order'),
    path('search/', product_search ,name='product_search'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]
