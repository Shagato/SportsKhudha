import json
from django.shortcuts import get_object_or_404
from .models import *

def get_or_create_customer(user):
    if not hasattr(user, 'customer'):
        customer = Customer.objects.create(user=user, email=user.email)
    else:
        customer = user.customer
    return customer

def get_cart_data(request):
    if request.user.is_authenticated:
        customer = get_or_create_customer(request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cart_data = get_cart_data_from_session(request)
        items = cart_data['items']
        order = {
            'get_cart_total': cart_data['total_cart_price'],
            'get_cart_items': cart_data['total_cart_items'],
            'shipping': False
        }
        cart_items = order['get_cart_items']
    return items, order, cart_items

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
