from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from datetime import datetime
from .models import *
from .utils import*
from django.core.paginator import Paginator
from django.db import transaction
from .forms import SearchForm, UserRegisterForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

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

    items, order, cart_items = get_cart_data(request)

    context = {'page_obj': page_obj, 'upcoming_products': upcoming_products, 'categories': categories, 'cartItems': cart_items}
    return render(request, 'pages/product_list.html', context)


def product_search(request):
    form = SearchForm()
    results = []
    query = ''

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(name__icontains=query)
    
    items, order, cart_items = get_cart_data(request)
    context = {'items': items, 'order': order, 'cartItems': cart_items,'form': form, 'query': query, 'results': results}

    return render(request, 'pages/product_search.html', context)

def register(request):
    form = UserRegisterForm()  # Initialize form outside the try-except block
    if request.method == 'POST':
        try:
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                # Save the user account
                user = form.save()
                username = form.cleaned_data.get('username')

                # Create a corresponding Customer object
                email = form.cleaned_data.get('email')
                customer = Customer.objects.create(user=user, email=email)

                # Log in the user
                login(request, user)
                
                # Redirect to the home page or any other desired page
                return redirect('home')
        except Exception as e:
            # Handle exceptions, such as form validation errors
            print(e)  # Print the error for debugging purposes

    return render(request, 'pages/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'pages/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def cart(request):
    items, order, cart_items = get_cart_data(request)
    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'pages/cart.html', context)


def checkout(request):
    items, order, cart_items = get_cart_data(request)
    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'pages/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = get_or_create_customer(request.user)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@transaction.atomic
def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = get_or_create_customer(request.user)
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
            OrderItem.objects.create(
                product=product,
                order=order,
                quantity=quantity
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if 'shipping' in data:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
