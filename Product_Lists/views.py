# views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, UpComingProducts, Category

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

    return render(request, 'pages/product_list.html', {'page_obj': page_obj, 'upcoming_products': upcoming_products, 'categories': categories})
