from django.shortcuts import render
from .models import Product 

def product_lists(request):
    products = Product.objects.order_by('-created_at')
    return render(request, 'pages/product_list.html', {'products': products})

      


