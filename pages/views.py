from django.shortcuts import render
from Product_Lists.models import *

def home(request):
    products = Product.objects.order_by('-created_at')
    upcoming_products = UpComingProducts.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    return render(request, 'pages/home.html', {'products': products, 'upcoming_products': upcoming_products,'cartItems':cartItems })




