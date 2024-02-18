from django.shortcuts import render
from .models import Product, UpComingProducts

def product_lists(request):
    
    products = Product.objects.order_by('-created_at')
    upcoming_products = UpComingProducts.objects.all()[:3] 
    if upcoming_products.count() < 3:
        upcoming_products = upcoming_products[:3]

    
    return render(request, 'pages/product_list.html', {'products': products, 'upcoming_products': upcoming_products})
