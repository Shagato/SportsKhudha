from django.shortcuts import render
from Product_Lists.models import Product, UpComingProducts

def home(request):
    products = Product.objects.order_by('-created_at')
    upcoming_products = UpComingProducts.objects.all()
    return render(request, 'pages/home.html', {'products': products, 'upcoming_products': upcoming_products})

def  cart(request):
    context = {}
    return render(request, 'pages/cart.html', context)

def checkout(request):
      context = {}
      return render(request, 'pages/checkout.html', context)