from django.shortcuts import render
from Product_Lists.models import Product

def home(request):
    products = Product.objects.order_by('-created_at')
    return render(request, 'pages/home.html', {'products': products})
