import json
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
import datetime

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

def product_lists(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_name = request.GET.get('category')

    products = Product.objects.order_by('-created_at')
    
    # Filter products by price range
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Filter products by category
    if category_name:
        products = products.filter(categories__name=category_name)

    categories = Category.objects.all()
    
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    upcoming_products = UpComingProducts.objects.all()[:3]
    if upcoming_products.count() < 3:
        upcoming_products = upcoming_products[:3]
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
         items = []
         order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
         cartItems = order['get_cart_items']

    
    context = {'page_obj': page_obj, 'upcoming_products': upcoming_products, 'categories': categories, 'cartItems': cartItems}
    return render(request, 'pages/product_list.html', context)

def cart(request):
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

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'pages/cart.html', context)




def checkout(request):
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

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'pages/checkout.html', context)


def update_item(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created  = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        name = data['form']['name']
        email = data['form']['email']

        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer=customer,
            complete=False,
        )

        for item in get_cart_data_from_session(request)['items']:
            product = item['product']
            quantity = item['quantity']
            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=quantity
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )

    return JsonResponse('Payment submitted..', safe=False)
