import json
from django.http import JsonResponse
from django.shortcuts import render
from Product_Lists.models import *
import datetime

def home(request):
    products = Product.objects.order_by('-created_at')
    upcoming_products = UpComingProducts.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cart_data = get_cart_data_from_session(request)
        items = cart_data['items']
        order = {
            'get_cart_total': cart_data['total_cart_price'],
            'get_cart_items': cart_data['total_cart_items'],
            'shipping': False
        }
        cartItems = order['get_cart_items']
    return render(request, 'pages/home.html', {'products': products, 'upcoming_products': upcoming_products,'cartItems':cartItems })


def get_cart_data_from_session(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    items = []
    total_cart_items = 0
    total_cart_price = 0

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total_price = product.price * item['quantity']
            items.append({
                'product': product,
                'quantity': item['quantity'],
                'get_total': total_price
            }) 
            total_cart_items += item['quantity']
            total_cart_price += total_price
        except Product.DoesNotExist:
            pass

    return {
        'items': items,
        'total_cart_items': total_cart_items,
        'total_cart_price': total_cart_price
    }

