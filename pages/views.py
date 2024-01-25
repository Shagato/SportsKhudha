from django.shortcuts import render
from Product_Lists.models import Product


# def home(request):
#     return render(request, 'pages/home.html')
def home(request):
    products = Product.objects.all()  
    return render(request, 'pages/home.html', {'products': products})